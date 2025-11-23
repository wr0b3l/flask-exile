# Pixel Bot - Start Backend Server
# Run this script to start the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pixel Bot - Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend virtual environment exists
if (-not (Test-Path "backend\venv\Scripts\python.exe")) {
    Write-Host "[ERROR] Backend virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: cd backend && python -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Dependencies checked" -ForegroundColor Green
Write-Host ""

# Start backend
Write-Host "[STARTING] Backend Server (Flask + Dashboard)..." -ForegroundColor Cyan
Write-Host ""

try {
    & backend\venv\Scripts\python.exe backend\app.py
}
catch {
    Write-Host ""
    Write-Host "[ERROR] Server crashed: $_" -ForegroundColor Red
}
finally {
    Write-Host ""
    Write-Host "[STOPPED] Server stopped" -ForegroundColor Yellow
}
