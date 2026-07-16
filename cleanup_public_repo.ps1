#requires -Version 5.1
<#
清理公开 GitHub 仓库，只保留网站运行与公开说明所需内容。

使用方法：
1. 把本脚本放到 D:\副业\game-map-web
2. 在 PowerShell 中运行：
   cd D:\副业\game-map-web
   Set-ExecutionPolicy -Scope Process Bypass
   .\cleanup_public_repo.ps1

脚本会：
- 创建一个仅保存在本地的备份分支
- 把开发脚本、日志、备份文件移动到仓库外的归档目录
- 删除旧的部署说明、复制图片脚本和重复图片
- 重写简洁 README.md
- 更新 .gitignore，防止杂乱文件再次提交
- 检查网站核心文件是否仍然完整
- 显示 Git 变更，确认后再提交并推送
#>

$ErrorActionPreference = "Stop"

function Write-Step([string]$Text) {
    Write-Host "`n==> $Text" -ForegroundColor Cyan
}

function Move-ToArchive([string]$RelativePath, [string]$ArchiveRoot) {
    $source = Join-Path (Get-Location) $RelativePath
    if (-not (Test-Path -LiteralPath $source)) {
        return
    }

    $destination = Join-Path $ArchiveRoot $RelativePath
    $destinationDir = Split-Path -Parent $destination
    New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null
    Move-Item -LiteralPath $source -Destination $destination -Force
    Write-Host "  已归档：$RelativePath" -ForegroundColor DarkGray
}

Write-Step "检查项目目录"

$repo = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $repo ".git"))) {
    throw "当前目录不是 Git 仓库。请先 cd 到 D:\副业\game-map-web。"
}

$requiredBefore = @(
    "index.html",
    "app.js",
    "style.css",
    "manifest.json",
    "assets"
)

foreach ($item in $requiredBefore) {
    if (-not (Test-Path -LiteralPath (Join-Path $repo $item))) {
        throw "缺少网站核心文件：$item。为避免误删，已停止。"
    }
}

$currentBranch = (git branch --show-current).Trim()
if ($currentBranch -ne "main") {
    throw "当前分支是 $currentBranch，不是 main。请先执行 git switch main。"
}

if ((git status --porcelain).Count -gt 0) {
    Write-Host "检测到本地还有未提交改动：" -ForegroundColor Yellow
    git status --short
    throw "请先确认并提交当前网站修改，再运行清理脚本。"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupBranch = "local-backup-before-public-cleanup-$timestamp"
$archiveRoot = Join-Path (Split-Path $repo -Parent) "game-map-web-dev-archive-$timestamp"

Write-Step "创建本地安全备份"
git branch $backupBranch
New-Item -ItemType Directory -Force -Path $archiveRoot | Out-Null
Write-Host "  本地备份分支：$backupBranch" -ForegroundColor Green
Write-Host "  开发文件归档：$archiveRoot" -ForegroundColor Green
Write-Host "  注意：备份分支不会自动推送到公开 GitHub。" -ForegroundColor Yellow

Write-Step "归档根目录开发文件"

$junkPatterns = @(
    "*.py",
    "*.log",
    "*.zip",
    "*.bak",
    "*backup*",
    "*broken*"
)

$junkFiles = @()
foreach ($pattern in $junkPatterns) {
    $junkFiles += Get-ChildItem -LiteralPath $repo -File -Filter $pattern -ErrorAction SilentlyContinue
}

$junkFiles = $junkFiles | Sort-Object FullName -Unique
foreach ($file in $junkFiles) {
    Move-ToArchive -RelativePath $file.Name -ArchiveRoot $archiveRoot
}

Write-Step "清理不需要公开的旧文件"

$explicitJunk = @(
    "DEPLOY.md",
    "copy_images_from_D.bat",
    "assets\details\右门\右-双L门.jpg"
)

foreach ($relative in $explicitJunk) {
    Move-ToArchive -RelativePath $relative -ArchiveRoot $archiveRoot
}

$cacheDirs = @(
    "__pycache__",
    ".pytest_cache"
)

foreach ($relative in $cacheDirs) {
    $source = Join-Path $repo $relative
    if (Test-Path -LiteralPath $source) {
        $destination = Join-Path $archiveRoot $relative
        Move-Item -LiteralPath $source -Destination $destination -Force
        Write-Host "  已归档：$relative" -ForegroundColor DarkGray
    }
}

Write-Step "写入公开版 README"

$readme = @'
# 第五人格地图小助手

一个适合手机使用的第五人格地图路线速查网页。

## 使用方法

从出门右侧的门进入，依据门的位置和特征，选择相应方向和地图。

## 作者

- 作者：cici吃饱饱
- 第五人格 ID：nku守门员
- 欢迎找我陪玩
- QQ：1405985556
- 邮箱：jayceja817@gmail.com

## 原创声明

本工具中的地图整理、路线规划、界面设计及标注内容均为原创制作，部分图片与视觉效果使用 AI 辅助增强。

本项目仅供个人自用与学习交流，不用于商业用途。未经允许，请勿搬运、转载或用于商业传播。

## 在线访问

https://140598cc180.github.io/game-map-helper/
'@

Set-Content -LiteralPath (Join-Path $repo "README.md") -Value $readme -Encoding UTF8

Write-Step "更新 .gitignore"

$gitignore = @'
# 开发脚本与日志
*.py
*.log
*.zip
*.bak
*backup*
*broken*
__pycache__/
.pytest_cache/

# 系统文件
.DS_Store
Thumbs.db

# 编辑器
.idea/
.vscode/
'@

Set-Content -LiteralPath (Join-Path $repo ".gitignore") -Value $gitignore -Encoding UTF8

Write-Step "再次检查网站核心文件"

$requiredAfter = @(
    "index.html",
    "app.js",
    "style.css",
    "manifest.json",
    ".nojekyll",
    "assets\avatar.png",
    "assets\icons\icon-192.png",
    "assets\icons\icon-512.png",
    "assets\details",
    "assets\thumbnails"
)

$missing = @()
foreach ($item in $requiredAfter) {
    if (-not (Test-Path -LiteralPath (Join-Path $repo $item))) {
        $missing += $item
    }
}

if ($missing.Count -gt 0) {
    Write-Host "缺少以下文件：" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    throw "核心文件检查失败。请执行 git reset --hard HEAD 恢复，或切换到本地备份分支。"
}

Write-Step "暂存清理结果"
git add -A

Write-Host "`n即将提交的文件变更：" -ForegroundColor Yellow
git status --short

Write-Host "`n保留的网站主体应包括：" -ForegroundColor Green
Write-Host "  assets/"
Write-Host "  index.html"
Write-Host "  app.js"
Write-Host "  style.css"
Write-Host "  manifest.json"
Write-Host "  .nojekyll"
Write-Host "  .gitignore"
Write-Host "  README.md"

$answer = Read-Host "`n确认以上内容无误并提交、推送到 GitHub？请输入 YES"

if ($answer -ne "YES") {
    Write-Host "已停止提交。变更仍处于暂存状态，可先检查。" -ForegroundColor Yellow
    Write-Host "取消本次清理可运行：git reset --hard HEAD" -ForegroundColor Yellow
    exit 0
}

Write-Step "提交并推送"
git commit -m "clean public website repository"
git push origin main

Write-Host "`n清理完成。" -ForegroundColor Green
Write-Host "网站地址：https://140598cc180.github.io/game-map-helper/?v=public-release" -ForegroundColor Green
Write-Host "本地开发文件归档：$archiveRoot" -ForegroundColor Green
Write-Host "本地备份分支：$backupBranch" -ForegroundColor Green
