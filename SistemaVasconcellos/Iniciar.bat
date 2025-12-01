@echo off
echo Iniciando sistema Vasconcellos...
start "" server.exe
timeout /t 2 >nul
start "" index.html

