@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist "地图系列小助手.exe" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
  if errorlevel 1 (
    echo 启动失败，请检查 build.ps1 的错误提示。
    pause
    exit /b 1
  )
)
start "" "%~dp0地图系列小助手.exe"
