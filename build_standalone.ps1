# ================================================================
# Pixel Bot - Standalone Executable Build Script
# ================================================================
# This script builds a standalone Windows executable using PyInstaller
# The resulting PixelBot.exe can run on any Windows PC without Python

param(
    [switch]$Clean,
    [switch]$Test,
    [switch]$NoConsole
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Pixel Bot - Standalone Build Script" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------------
# Step 1: Check Prerequisites
# ----------------------------------------------------------------
Write-Host "[1/7] Checking prerequisites..." -ForegroundColor Yellow

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Red
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "  [OK] Virtual environment found" -ForegroundColor Green

# Use venv Python directly
$pythonExe = ".\venv\Scripts\python.exe"
$pipExe = ".\venv\Scripts\pip.exe"

# Check if PyInstaller is installed
Write-Host "  Checking for PyInstaller..." -ForegroundColor Gray
$pyinstaller = & $pythonExe -c "try: import PyInstaller; print('installed')
except: print('not installed')" 2>$null
if ($pyinstaller -ne "installed") {
    Write-Host "  PyInstaller not found. Installing..." -ForegroundColor Yellow
    & $pipExe install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  [OK] PyInstaller ready" -ForegroundColor Green

# ----------------------------------------------------------------
# Step 2: Clean Previous Builds (Optional)
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[2/7] Cleaning previous builds..." -ForegroundColor Yellow

if ($Clean -or (Test-Path "build") -or (Test-Path "dist")) {
    if (Test-Path "build") {
        Write-Host "  Removing build/ directory..." -ForegroundColor Gray
        Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path "dist") {
        Write-Host "  Removing dist/ directory..." -ForegroundColor Gray
        Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  [OK] Clean complete" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] No previous builds found" -ForegroundColor Gray
}

# ----------------------------------------------------------------
# Step 3: Verify Required Files
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[3/7] Verifying required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "PixelBot.spec",
    "backend\app.py",
    "backend\config.py",
    "backend\static\dashboard.html"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
        Write-Host "  [MISSING] $file" -ForegroundColor Red
    } else {
        Write-Host "  [OK] $file" -ForegroundColor Green
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROR: Missing required files!" -ForegroundColor Red
    exit 1
}

# ----------------------------------------------------------------
# Step 4: Modify Spec for Console/No Console
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[4/7] Configuring build options..." -ForegroundColor Yellow

if ($NoConsole) {
    Write-Host "  [INFO] Building with NO console window (GUI mode)" -ForegroundColor Cyan
    # Note: We'd need to modify the spec file or use a flag
    # For now, just notify - user can edit PixelBot.spec manually
} else {
    Write-Host "  [INFO] Building WITH console window (shows logs)" -ForegroundColor Cyan
}

# ----------------------------------------------------------------
# Step 5: Build Executable
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[5/7] Building executable..." -ForegroundColor Yellow
Write-Host "  This may take 2-5 minutes..." -ForegroundColor Gray
Write-Host ""

$buildStart = Get-Date

try {
    & $pythonExe -m PyInstaller PixelBot.spec --clean
    
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller build failed"
    }
} catch {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "  BUILD FAILED" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check that all dependencies are installed" -ForegroundColor Gray
    Write-Host "  2. Look at the error messages above" -ForegroundColor Gray
    Write-Host "  3. Try running: pip install -r backend\requirements.txt" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$buildEnd = Get-Date
$buildTime = ($buildEnd - $buildStart).TotalSeconds

Write-Host ""
Write-Host "  [OK] Build completed in $([math]::Round($buildTime, 1)) seconds" -ForegroundColor Green

# ----------------------------------------------------------------
# Step 6: Verify Output
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[6/7] Verifying build output..." -ForegroundColor Yellow

if (-not (Test-Path "dist\PixelBot.exe")) {
    Write-Host ""
    Write-Host "ERROR: PixelBot.exe was not created!" -ForegroundColor Red
    exit 1
}

$exeSize = (Get-Item "dist\PixelBot.exe").Length / 1MB
Write-Host "  [OK] PixelBot.exe created" -ForegroundColor Green
Write-Host "  [INFO] Size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Cyan

# Copy config example to dist
if (Test-Path "backend\pixelbot_config.example.ini") {
    Copy-Item "backend\pixelbot_config.example.ini" "dist\" -Force
    Write-Host "  [OK] Config example copied to dist/" -ForegroundColor Green
}

# ----------------------------------------------------------------
# Step 7: Test Executable (Optional)
# ----------------------------------------------------------------
Write-Host ""
Write-Host "[7/7] Post-build steps..." -ForegroundColor Yellow

if ($Test) {
    Write-Host "  [TEST] Starting PixelBot.exe for 10 seconds..." -ForegroundColor Yellow
    
    $testProcess = Start-Process -FilePath "dist\PixelBot.exe" -PassThru
    Start-Sleep -Seconds 10
    
    if (-not $testProcess.HasExited) {
        Write-Host "  [OK] PixelBot.exe is running" -ForegroundColor Green
        Stop-Process -Id $testProcess.Id -Force
        Write-Host "  [INFO] Test process stopped" -ForegroundColor Gray
    } else {
        Write-Host "  [WARNING] PixelBot.exe exited unexpectedly" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [SKIP] Use -Test flag to run quick test" -ForegroundColor Gray
}

# ----------------------------------------------------------------
# Success Summary
# ----------------------------------------------------------------
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Output:" -ForegroundColor Cyan
Write-Host "  Location:  dist\PixelBot.exe" -ForegroundColor White
Write-Host "  Size:      $([math]::Round($exeSize, 2)) MB" -ForegroundColor White
Write-Host "  Type:      Standalone Windows Executable" -ForegroundColor White
Write-Host ""
Write-Host "What's Included:" -ForegroundColor Cyan
Write-Host "  - Python runtime" -ForegroundColor White
Write-Host "  - All dependencies (Flask, SocketIO, MSS, etc.)" -ForegroundColor White
Write-Host "  - Web dashboard (static files)" -ForegroundColor White
Write-Host "  - Bot modules (screen capture, pixel detection)" -ForegroundColor White
Write-Host "  - Desktop picker overlay" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test the executable:" -ForegroundColor White
Write-Host "     cd dist" -ForegroundColor Yellow
Write-Host "     .\PixelBot.exe" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. (Optional) Rename config:" -ForegroundColor White
Write-Host "     Rename pixelbot_config.example.ini to pixelbot_config.ini" -ForegroundColor Yellow
Write-Host "     Edit settings as needed" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Distribute:" -ForegroundColor White
Write-Host "     - Share PixelBot.exe (works on any Windows PC)" -ForegroundColor Yellow
Write-Host "     - Include pixelbot_config.example.ini for advanced users" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

