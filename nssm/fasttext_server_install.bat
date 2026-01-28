@echo off
chcp 65001 >nul

set NSSM=C:\nssm\win64\nssm.exe
set SERVICE_NAME=fasttext_server
set PYTHON_EXE=E:\WebServer\fastText\venv\Scripts\python.exe
set FASTTEXT_SERVER_CONF=-m uvicorn fasttext_server:app --host 127.0.0.1 --port 9231 --workers 2

echo [INFO] 安装服务 %SERVICE_NAME%...
"%NSSM%" install "%SERVICE_NAME%" "%PYTHON_EXE%"
"%NSSM%" set "%SERVICE_NAME%" AppParameters "%FASTTEXT_SERVER_CONF%"
"%NSSM%" set "%SERVICE_NAME%" AppDirectory E:\WebServer\fastText
"%NSSM%" set "%SERVICE_NAME%" AppRestartDelay 5000
"%NSSM%" set "%SERVICE_NAME%" AppThrottle 1500
echo [OK] 安装完成。

echo [INFO] 启动服务 %SERVICE_NAME%...
net start "%SERVICE_NAME%"

pause
