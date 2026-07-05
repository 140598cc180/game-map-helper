@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在创建图片目录...
if not exist "assets\thumbnails" mkdir "assets\thumbnails"
if not exist "assets\details" mkdir "assets\details"

echo.
echo 正在复制缩略图...
xcopy "D:\BaiduNetdiskDownload\缩略图\*" "assets\thumbnails\" /E /I /Y

echo.
echo 正在复制详细图...
xcopy "D:\BaiduNetdiskDownload\详细图\*" "assets\details\" /E /I /Y

echo.
echo 图片复制完成。
pause
