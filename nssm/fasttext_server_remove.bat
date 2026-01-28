@echo off
chcp 65001 >nul

set NSSM=C:\nssm\win64\nssm.exe
set SERVICE_NAME=fasttext_server

echo [INFO] 卸载服务 %SERVICE_NAME%...
"%NSSM%" stop "%SERVICE_NAME%" >nul 2>&1
"%NSSM%" remove "%SERVICE_NAME%" confirm
echo [OK] 已卸载。

pause
