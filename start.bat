@echo off
setlocal

where uv >nul 2>&1
if errorlevel 1 (
    echo uv is not installed. Install it first:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 ^| iex"
    pause
    exit /b 1
)

uv sync --quiet
uv run pixelbot %*
