#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Set-Location -LiteralPath $PSScriptRoot
$candidates = @(
    (Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'),
    (Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe')
)
$compiler = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $compiler) { throw 'The Windows .NET Framework C# compiler was not found.' }
$output = Join-Path $PSScriptRoot '地图系列小助手.exe'
$arguments = @(
    '/nologo', '/target:winexe', '/platform:anycpu', '/optimize+', '/utf8output',
    ('/out:' + $output), '/reference:System.dll', '/reference:System.Core.dll',
    '/reference:System.Drawing.dll', '/reference:System.Windows.Forms.dll', '/reference:System.Web.Extensions.dll',
    '/resource:index.html,index.html', '/resource:app.js,app.js', '/resource:style.css,style.css', '/resource:manifest.json,manifest.json', 'MapHelper.cs'
)
& $compiler @arguments
if ($LASTEXITCODE -ne 0) { throw 'Build failed. Exit the running EXE from its tray menu before rebuilding.' }
$process = Start-Process -FilePath $output -ArgumentList '--export-catalog' -Wait -PassThru -WindowStyle Hidden
if ($process.ExitCode -ne 0) { throw 'Catalog export failed.' }
Write-Host ('Built: ' + $output) -ForegroundColor Green
Write-Host '图片清单已写入 catalog.js。更新地图图片后，请重新生成对应的离线版本。'
