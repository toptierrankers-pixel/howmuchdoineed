@echo off
REM Runs the site generator and keeps the window open so you can read the output.
cd /d "%~dp0"
py build.py 2>nul || python build.py
echo.
echo Done. Press any key to close.
pause >nul
