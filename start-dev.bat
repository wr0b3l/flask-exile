@echo off
REM Pixel Bot - Start Development Server
REM Simple batch script for Windows

echo ========================================
echo   Pixel Bot - Starting Application
echo ========================================
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv\Scripts\python.exe" (
    echo [ERROR] Backend virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv venv ^&^& .\venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] Dependencies checked
echo.

REM Start backend
echo [STARTING] Backend Server (Flask + Dashboard)...
echo.
echo ========================================
echo   APPLICATION RUNNING!
echo ========================================
echo.
echo Dashboard: http://localhost:5000
echo API:       http://localhost:5000/api/status
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd backend
venv\Scripts\python.exe app.py

echo.
echo [STOPPED] Server stopped
echo.
pause
