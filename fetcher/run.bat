@echo off
chcp 65001 >nul
cd /d "%~dp0"
"C:\Users\jiamingliang\AppData\Local\Programs\Python\Python312\python.exe" fetch_news.py
exit /b %ERRORLEVEL%
