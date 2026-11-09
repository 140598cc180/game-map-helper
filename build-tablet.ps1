#requires -Version 5.1
param(
    [switch]$PrepareOnly,
    [switch]$Offline,
    [switch]$RunLint
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = [IO.Path]::GetFullPath($PSScriptRoot)
$Project = Join-Path $Root 'android-tablet'
$Stage = Join-Path $Project 'app\src\main\assets\www'
$Utf8 = New-Object Text.UTF8Encoding($false)

function Step([string]$Text) { Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Write-Utf8([string]$Path, [string]$Text) { [IO.File]::WriteAllText($Path, $Text, $Utf8) }

function Find-Image([string]$Folder, [string]$Stem) {
    if (-not (Test-Path -LiteralPath $Folder -PathType Container)) { return $null }
    $Files = @(Get-ChildItem -LiteralPath $Folder -File)
    foreach ($Extension in @('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')) {
        $Image = $Files | Where-Object { $_.BaseName -ieq $Stem -and $_.Extension -ieq $Extension -and $_.Length -gt 0 } | Select-Object -First 1
        if ($Image) {
            $Relative = $Image.FullName.Substring($Root.Length + 1)
            $Destination = Join-Path $Stage $Relative
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Destination))
            Copy-Item -LiteralPath $Image.FullName -Destination $Destination -Force
            $Parts = @($Relative.Replace('\', '/').Split('/') | ForEach-Object { [Uri]::EscapeDataString($_) })
            return './' + ($Parts -join '/')
        }
    }
    return $null
}

Step 'Synchronize current website and map images'
foreach ($Name in @('index.html', 'app.js', 'style.css', 'series\nightmare-woman\catalog.json')) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $Name))) { throw "Missing website file: $Name" }
}
$ResolvedStage = [IO.Path]::GetFullPath($Stage)
$ExpectedStage = [IO.Path]::GetFullPath((Join-Path $Project 'app\src\main\assets\www'))
if ($ResolvedStage -ne $ExpectedStage -or -not $ResolvedStage.StartsWith($Project + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe generated-assets path.' }
if (Test-Path -LiteralPath $Stage) { Remove-Item -LiteralPath $Stage -Recurse -Force }
[void][IO.Directory]::CreateDirectory($Stage)
foreach ($Name in @('index.html', 'app.js', 'style.css', 'manifest.json')) { Copy-Item -LiteralPath (Join-Path $Root $Name) -Destination $Stage -Force }
foreach ($Folder in @('icos', 'assets')) {
    $SourceFolder = Join-Path $Root $Folder
    if (Test-Path -LiteralPath $SourceFolder -PathType Container) {
        Copy-Item -LiteralPath $SourceFolder -Destination $Stage -Recurse -Force
    }
}

$LegacyJson = [IO.File]::ReadAllText((Join-Path $Root 'series\nightmare-woman\catalog.json'), [Text.Encoding]::UTF8)
$LegacySeries = $LegacyJson | ConvertFrom-Json
$LegacyAssetSource = Join-Path $Root 'series\nightmare-woman\assets'
$LegacyAssetDestination = Join-Path $Stage 'series\nightmare-woman\assets'
[void][IO.Directory]::CreateDirectory($LegacyAssetDestination)
foreach ($Entry in Get-ChildItem -LiteralPath $LegacyAssetSource -Force) {
    Copy-Item -LiteralPath $Entry.FullName -Destination $LegacyAssetDestination -Recurse -Force
}

$Labels = @('类别一', '类别二', '类别三', '类别四', '类别五', '类别六')
$Categories = @()
for ($Number = 1; $Number -le 6; $Number++) {
    $ClassId = 'class' + $Number
    $ClassRoot = Join-Path $Root $ClassId
    $Maps = @()
    $Folders = @()
    if (Test-Path -LiteralPath $ClassRoot) {
        $Folders = @(Get-ChildItem -LiteralPath $ClassRoot -Directory | Where-Object { $_.Name -match '^map([1-9][0-9]*)$' -and $_.Name.Length -lt 13 } | Sort-Object { [int]$_.Name.Substring(3) })
    }
    foreach ($Folder in $Folders) {
        $MapNumber = [int]$Folder.Name.Substring(3)
        $Stem = 'c' + $Number + 'm' + $MapNumber
        $Maps += [ordered]@{
            id = 'map' + $MapNumber
            number = $MapNumber
            label = '地图 ' + $MapNumber
            thumbnail = Find-Image $Folder.FullName ($Stem + 'thumbnail')
            detail = Find-Image $Folder.FullName ($Stem + 'detail')
        }
    }
    $Categories += [ordered]@{
        id = $ClassId
        number = $Number
        label = $Labels[$Number - 1]
        thumbnail = Find-Image (Join-Path $Root 'classimage') ('c' + $Number + 'thumbnail')
        maps = @($Maps)
    }
}
$PhosphorSeries = [ordered]@{
    id = 'phosphor'
    label = '磷光症'
    difficulty = '噩梦难度'
    lastUpdated = '11.8'
    theme = 'phosphor'
    classes = @($Categories)
}
$Catalog = [ordered]@{ series = @($LegacySeries, $PhosphorSeries) }
$CatalogJson = ConvertTo-Json -InputObject $Catalog -Depth 12 -Compress
Write-Utf8 (Join-Path $Stage 'catalog.js') ('window.MAP_RUNTIME = "android";' + "`nwindow.MAP_CATALOG = " + $CatalogJson + ";`n")
$AllMaps = @($Catalog.series | ForEach-Object { $_.classes | ForEach-Object { $_.maps } })
$Ready = @($AllMaps | Where-Object { $_.detail }).Count
$MapCount = $AllMaps.Count
$CategoryCount = @($Catalog.series | ForEach-Object { $_.classes }).Count
Write-Host "Series: 2; categories: $CategoryCount; maps: $MapCount; ready: $Ready"
if ($PrepareOnly) { Write-Host "Prepared assets: $Stage"; return }

Step 'Locate Java, Android SDK, and Gradle'
$JdkCandidates = @()
if ($env:JAVA_HOME) { $JdkCandidates += $env:JAVA_HOME }
$JdkCandidates += @(
    (Join-Path $env:ProgramFiles 'Android\Android Studio\jbr'),
    (Join-Path $env:LOCALAPPDATA 'Programs\Android Studio\jbr')
)
$JavaCommand = Get-Command java.exe -ErrorAction SilentlyContinue
if ($JavaCommand) { $JdkCandidates += Split-Path -Parent (Split-Path -Parent $JavaCommand.Source) }
$Jdk = $JdkCandidates | Where-Object { $_ -and (Test-Path -LiteralPath (Join-Path $_ 'bin\javac.exe')) } | Select-Object -First 1
if (-not $Jdk) { throw 'No JDK found. Install Android Studio or set JAVA_HOME.' }
$env:JAVA_HOME = $Jdk
# Keep Java's local socket files out of virtualized AppData temp folders.
$SocketDir = Join-Path $Root '.android-build\sockets'
[void][IO.Directory]::CreateDirectory($SocketDir)
$env:JAVA_TOOL_OPTIONS = ($env:JAVA_TOOL_OPTIONS + ' "-Djdk.net.unixdomain.tmpdir=' + $SocketDir + '"').Trim()

$SdkCandidates = @()
if ($env:ANDROID_HOME) { $SdkCandidates += $env:ANDROID_HOME }
if ($env:ANDROID_SDK_ROOT) { $SdkCandidates += $env:ANDROID_SDK_ROOT }
$SdkCandidates += Join-Path $env:LOCALAPPDATA 'Android\Sdk'
$Sdk = $SdkCandidates | Where-Object { $_ -and (Test-Path -LiteralPath (Join-Path $_ 'platforms\android-36\android.jar')) } | Select-Object -First 1
if (-not $Sdk) { throw 'Android SDK 36 is missing. Install it using Android Studio SDK Manager.' }
Write-Utf8 (Join-Path $Project 'local.properties') ('sdk.dir=' + $Sdk.Replace('\', '/') + "`n")

$GradleHome = if ($env:GRADLE_USER_HOME) { $env:GRADLE_USER_HOME } else { Join-Path $env:USERPROFILE '.gradle' }
$Distribution = Join-Path $GradleHome 'wrapper\dists\gradle-9.3.0-bin'
$Cached = @(Get-ChildItem -LiteralPath $Distribution -Filter gradle.bat -Recurse -ErrorAction SilentlyContinue | Sort-Object FullName)
if ($Cached.Count -gt 0) { $Gradle = $Cached[0].FullName }
elseif (Test-Path -LiteralPath (Join-Path $Project 'gradlew.bat')) { $Gradle = Join-Path $Project 'gradlew.bat' }
else {
    $GradleCommand = Get-Command gradle.bat -ErrorAction SilentlyContinue
    if (-not $GradleCommand) { throw 'Gradle 9.3.0 was not found. Open android-tablet in Android Studio to configure Gradle.' }
    $Gradle = $GradleCommand.Source
}

Step 'Keep a stable signing key for future tablet updates'
$SignDir = Join-Path $Project '.signing'
[void][IO.Directory]::CreateDirectory($SignDir)
$Key = Join-Path $SignDir 'maphelper.keystore'
if (-not (Test-Path -LiteralPath $Key)) {
    & (Join-Path $Jdk 'bin\keytool.exe') -genkeypair -keystore $Key -storetype PKCS12 -alias maphelper -storepass android -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname 'CN=Phosphor Map Helper, O=Local Maps, C=CN' -noprompt
    if ($LASTEXITCODE -ne 0) { throw 'Signing-key generation failed.' }
}

$VersionFile = Join-Path $Project 'version.properties'
$CurrentVersion = [IO.File]::ReadAllText($VersionFile)
$VersionMatch = [regex]::Match($CurrentVersion, '(?m)^versionCode=(\d+)')
$Version = if ($VersionMatch.Success) { [int]$VersionMatch.Groups[1].Value + 1 } else { 1 }
Write-Utf8 $VersionFile ("versionCode=$Version`nversionName=1.0.$Version`n")

Step 'Build and check the installable APK'
$Arguments = @('wrapper', 'assembleDebug', '--no-daemon', '--console=plain')
if ($RunLint) { $Arguments += 'lintDebug' }
if ($Offline) { $Arguments += '--offline' }
Push-Location $Project
try {
    & $Gradle @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Android build failed, exit code $LASTEXITCODE" }
} finally { Pop-Location }

$SourceApk = Join-Path $Project 'app\build\outputs\apk\debug\app-debug.apk'
if (-not (Test-Path -LiteralPath $SourceApk)) { throw 'Gradle did not produce an APK.' }
$ApkSigner = Join-Path $Sdk 'build-tools\36.0.0\apksigner.bat'
& $ApkSigner verify --verbose $SourceApk
if ($LASTEXITCODE -ne 0) { throw 'APK signature verification failed.' }
$Release = Join-Path $Root 'release'
[void][IO.Directory]::CreateDirectory($Release)
$FinalApk = Join-Path $Release '地图系列小助手-安卓版.apk'
Copy-Item -LiteralPath $SourceApk -Destination $FinalApk -Force
$Hash = (Get-FileHash -LiteralPath $FinalApk -Algorithm SHA256).Hash
$Info = [ordered]@{
    applicationId = 'com.phosphor.maphelper'
    appName = '地图系列小助手'
    versionCode = $Version
    versionName = "1.0.$Version"
    apk = [IO.Path]::GetFileName($FinalApk)
    sha256 = $Hash
    minimumAndroidApi = 24
    series = 2
    categories = $CategoryCount
    maps = $MapCount
    ready = $Ready
    offline = $true
}
Write-Utf8 (Join-Path $Release 'apk-info.json') (ConvertTo-Json -InputObject $Info -Depth 6)
Write-Utf8 (Join-Path $Release 'SHA256.txt') ($Hash + '  ' + [IO.Path]::GetFileName($FinalApk) + "`n")
Write-Host "`nAPK: $FinalApk" -ForegroundColor Green
Write-Host 'Send this APK to the Android tablet and open it to install.'
Write-Host 'Keep android-tablet/.signing/maphelper.keystore so later builds can update this installation.'
