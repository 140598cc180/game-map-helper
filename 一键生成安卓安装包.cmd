@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-tablet.ps1"
if errorlevel 1 (
  echo 安卓安装包生成失败，请查看上面的错误信息。
  pause
  exit /b 1
)
echo 安装包已生成在 release 文件夹。
pause
