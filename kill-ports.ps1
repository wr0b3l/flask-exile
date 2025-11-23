# Pixel Bot - Kill Ports Script
# Use this to free up ports 3000 and 5000 if they're stuck

Write-Host "Checking ports..." -ForegroundColor Cyan

# Check port 5000
$port5000 = netstat -ano | findstr :5000
if ($port5000) {
    Write-Host "Port 5000 is in use:" -ForegroundColor Yellow
    Write-Host $port5000
    $pid5000 = ($port5000 -split '\s+')[-1]
    Write-Host "Killing process $pid5000..." -ForegroundColor Red
    taskkill /F /PID $pid5000 2>$null
}

# Check port 3000
$port3000 = netstat -ano | findstr :3000
if ($port3000) {
    Write-Host "Port 3000 is in use:" -ForegroundColor Yellow
    Write-Host $port3000
    $pid3000 = ($port3000 -split '\s+')[-1]
    Write-Host "Killing process $pid3000..." -ForegroundColor Red
    taskkill /F /PID $pid3000 2>$null
}

Write-Host "`nPorts cleared! You can now run start-dev.ps1" -ForegroundColor Green

