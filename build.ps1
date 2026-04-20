# Build PixelBot.exe using uv + PyInstaller.
# Usage: .\build.ps1        (clean build, single-file .exe at dist\PixelBot.exe)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "Building Pixel Bot standalone executable..." -ForegroundColor Cyan
Write-Host ""

# Check uv is available (it auto-installs Python if needed).
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: uv is not installed." -ForegroundColor Red
    Write-Host "Install it from https://docs.astral.sh/uv/getting-started/installation/"
    Write-Host "Or run: powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
    exit 1
}

# Sync build deps (includes pyinstaller via the [build] extra).
Write-Host "[1/3] Syncing dependencies..." -ForegroundColor Yellow
uv sync --extra build

# Clean previous artifacts.
Write-Host "[2/3] Cleaning previous build output..." -ForegroundColor Yellow
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }

# Invoke PyInstaller through uv so it picks up the project venv.
Write-Host "[3/3] Running PyInstaller..." -ForegroundColor Yellow
uv run pyinstaller PixelBot.spec --clean --noconfirm

if (Test-Path dist\PixelBot.exe) {
    $sizeMB = [math]::Round((Get-Item dist\PixelBot.exe).Length / 1MB, 1)
    Write-Host ""
    Write-Host "Done. dist\PixelBot.exe ($sizeMB MB)" -ForegroundColor Green
} else {
    Write-Host "Build finished but dist\PixelBot.exe was not produced." -ForegroundColor Red
    exit 1
}
