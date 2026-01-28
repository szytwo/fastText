@echo off
chcp 65001 >nul

set SERVICE_NAME=fasttext_server

echo [INFO] 停止服务 %SERVICE_NAME%...
net stop "%SERVICE_NAME%"

pause
