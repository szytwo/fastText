@echo off
chcp 65001 >nul

set SERVICE_NAME=fasttext_server

echo [INFO] 启动服务 %SERVICE_NAME%...
net start "%SERVICE_NAME%"

pause
