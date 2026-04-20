# Launch Pixel Bot in a native window.
# Requires uv (https://docs.astral.sh/uv/). uv will auto-install the right Python version.

$ErrorActionPreference = "Stop"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv is not installed. Install it first:" -ForegroundColor Yellow
    Write-Host '  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"' -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

# uv sync is idempotent — cheap on subsequent runs.
uv sync --quiet
uv run pixelbot @args
