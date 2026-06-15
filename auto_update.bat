@echo off
setlocal
REM ============================================================
REM Q3 2026 daily auto-update
REM 1) run fetch_news.py (RSS -> DeepSeek -> news.json)
REM 2) if news.json changed, git commit + push to GitHub
REM    Vercel will auto-redeploy on push.
REM ============================================================
cd /d "%~dp0"

REM --- log header ---
if not exist logs mkdir logs
set LOGFILE=logs\auto_update_%date:~0,4%-%date:~5,2%-%date:~8,2%.log
echo. >> "%LOGFILE%"
echo ============================================================ >> "%LOGFILE%"
echo [%date% %time%] auto_update start >> "%LOGFILE%"

REM --- run fetcher ---
echo [%date% %time%] running fetch_news.py >> "%LOGFILE%"
pushd fetcher
python fetch_news.py >> "..\%LOGFILE%" 2>&1
set FETCH_RC=%ERRORLEVEL%
popd

if %FETCH_RC% NEQ 0 (
  echo [%date% %time%] FATAL: fetch_news.py exit %FETCH_RC% >> "%LOGFILE%"
  exit /b %FETCH_RC%
)

REM --- check if news.json changed ---
git diff --quiet news.json
if %ERRORLEVEL% EQU 0 (
  echo [%date% %time%] news.json unchanged, skip push >> "%LOGFILE%"
  exit /b 0
)

REM --- commit + push ---
echo [%date% %time%] news.json changed, committing >> "%LOGFILE%"
git add news.json >> "%LOGFILE%" 2>&1
git -c user.email="auto@local" -c user.name="K4MING-LEUNG" commit -m "daily: news %date:~0,4%-%date:~5,2%-%date:~8,2%" >> "%LOGFILE%" 2>&1
git push origin main >> "%LOGFILE%" 2>&1
set PUSH_RC=%ERRORLEVEL%

if %PUSH_RC% NEQ 0 (
  echo [%date% %time%] FATAL: git push exit %PUSH_RC% >> "%LOGFILE%"
  exit /b %PUSH_RC%
)

echo [%date% %time%] done, Vercel will redeploy >> "%LOGFILE%"
exit /b 0
