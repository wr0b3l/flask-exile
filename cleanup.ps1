# Pixel Bot - Cleanup Script
# Removes unnecessary files and organizes the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pixel Bot - Project Cleanup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$itemsToRemove = @()
$itemsToKeep = @()

# Check what can be removed
Write-Host "Scanning project..." -ForegroundColor Yellow
Write-Host ""

# Frontend (React) - No longer needed
if (Test-Path "frontend") {
    $itemsToRemove += "frontend/ (React app - replaced by simple HTML)"
}

# Old HTML interface
if (Test-Path "backend\static\index.html") {
    $itemsToRemove += "backend\static\index.html (old interface)"
}

# Input controller (unused Node.js project)
if (Test-Path "input-controller") {
    $itemsToRemove += "input-controller/ (unused Node.js project)"
}

# Temporary/redundant documentation
$docsToCheck = @(
    "SETUP_COMPLETE.md",
    "TEST_RESULTS_SUMMARY.txt",
    "QUICKSTART.md",
    "THREADING_FIX.txt",
    "PICKER_FIX.txt",
    "WEB_UI_FIX.txt",
    "DEV_SCRIPTS_GUIDE.txt",
    "IMPORT_WARNINGS_FIX.md",
    "UNRESOLVED_IMPORTS_EXPLAINED.txt",
    "FINAL_SUCCESS_REPORT.txt",
    "REACT_FRONTEND_SETUP.txt",
    "INSTALLATION_REPORT.txt"
)

foreach ($doc in $docsToCheck) {
    if (Test-Path $doc) {
        $itemsToRemove += $doc
    }
}

# Show what will be removed
Write-Host "Items to REMOVE:" -ForegroundColor Red
Write-Host "=================" -ForegroundColor Red
foreach ($item in $itemsToRemove) {
    Write-Host "  [X] $item" -ForegroundColor Red
}

Write-Host ""
Write-Host "Items to KEEP:" -ForegroundColor Green
Write-Host "==============" -ForegroundColor Green
$keepList = @(
    "backend/ (Flask server + all tools)",
    "  ├── app.py (API + WebSocket server)",
    "  ├── desktop_picker.py (pixel picker)",
    "  ├── pixel_monitor.py (monitoring)",
    "  ├── bot/ (automation modules)",
    "  └── static/dashboard.html (UI)",
    "README.md (main documentation)",
    "ARCHITECTURE.md (system design)",
    "ARCHITECTURAL_REDESIGN.txt (design decisions)",
    "SIMPLIFIED_ARCHITECTURE.txt (final architecture)",
    "start-dev.ps1 (launch script)",
    "start-dev.py (cross-platform launcher)",
    "start-dev.bat (simple launcher)",
    "kill-ports.ps1 (port cleanup utility)"
)
foreach ($item in $keepList) {
    Write-Host "  [+] $item" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
$confirmation = Read-Host "Proceed with cleanup? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "Cleanup cancelled" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Starting cleanup..." -ForegroundColor Cyan

# Remove frontend directory
if (Test-Path "frontend") {
    Write-Host "Removing frontend/ directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "frontend" -ErrorAction SilentlyContinue
    Write-Host "  [OK] Removed frontend/" -ForegroundColor Green
}

# Remove old index.html
if (Test-Path "backend\static\index.html") {
    Write-Host "Removing old index.html..." -ForegroundColor Yellow
    Remove-Item -Force "backend\static\index.html" -ErrorAction SilentlyContinue
    Write-Host "  [OK] Removed backend\static\index.html" -ForegroundColor Green
}

# Remove input-controller
if (Test-Path "input-controller") {
    Write-Host "Removing input-controller/ directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "input-controller" -ErrorAction SilentlyContinue
    Write-Host "  [OK] Removed input-controller/" -ForegroundColor Green
}

# Create docs archive directory
if (-not (Test-Path "docs_archive")) {
    New-Item -ItemType Directory -Path "docs_archive" | Out-Null
}

# Move redundant docs to archive
foreach ($doc in $docsToCheck) {
    if (Test-Path $doc) {
        Write-Host "Archiving $doc..." -ForegroundColor Yellow
        Move-Item -Path $doc -Destination "docs_archive\" -Force -ErrorAction SilentlyContinue
        Write-Host "  [OK] Moved to docs_archive/" -ForegroundColor Green
    }
}

# Remove test files
$testFiles = @(
    "test_comprehensive.py",
    "test_imports.py",
    "test_ocr.py",
    "examples.py"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Write-Host "Removing $file..." -ForegroundColor Yellow
        Remove-Item -Force $file -ErrorAction SilentlyContinue
        Write-Host "  [OK] Removed $file" -ForegroundColor Green
    }
}

# Clean up pycache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  [OK] Removed __pycache__ directories" -ForegroundColor Green

# Clean up test screenshots
if (Test-Path "screenshots") {
    $screenshotCount = (Get-ChildItem "screenshots" -File).Count
    if ($screenshotCount -gt 0) {
        Remove-Item "screenshots\*" -Force -ErrorAction SilentlyContinue
        Write-Host "  [OK] Cleaned screenshots directory" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Cleanup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Project is now clean and organized!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current structure:" -ForegroundColor Yellow
Write-Host "  potta/" -ForegroundColor White
Write-Host "  ├── backend/" -ForegroundColor White
Write-Host "  │   ├── app.py              (Flask server)" -ForegroundColor White
Write-Host "  │   ├── desktop_picker.py   (pixel picker)" -ForegroundColor White
Write-Host "  │   ├── pixel_monitor.py    (monitoring)" -ForegroundColor White
Write-Host "  │   ├── bot/                (modules)" -ForegroundColor White
Write-Host "  │   └── static/dashboard.html" -ForegroundColor White
Write-Host "  ├── start-dev.ps1           (launcher)" -ForegroundColor White
Write-Host "  └── README.md               (documentation)" -ForegroundColor White
Write-Host ""
Write-Host "Ready to use! Run: .\start-dev.ps1" -ForegroundColor Cyan
Write-Host ""
