# Pixel Bot — Desktop Automation Helper

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A lightweight desktop automation helper for Windows. Watches pixels on the screen and fires keyboard actions when they change. Built with Path of Exile in mind, but works for any game or workflow.

![Pixel Bot](backend/static/images/logo.png)

## Features

- **Pixel monitoring** with configurable color tolerance
- **Desktop pixel picker** — system-wide overlay to grab coordinates and colors
- **Keyboard / hotkey actions** with per-monitor cooldowns
- **Master/slave monitors** — gate slaves on a master condition (e.g. only fire flasks if the UI is visible)
- **Multi-pixel checks** with AND / OR logic
- **Native desktop window** (via PyWebView) — no browser tab, no localhost fiddling
- **Persistent config** in a single JSON file

## Quick start

### 1. Install `uv`

`uv` manages Python versions and dependencies. It will fetch the right Python for you — **you do not need Python on PATH**.

PowerShell:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Or see [uv install docs](https://docs.astral.sh/uv/getting-started/installation/).

### 2. Run

```powershell
# From the repo root
.\start.ps1
```

or simply double-click **`start.bat`**.

That's it. `uv` auto-creates a `.venv`, installs deps, and opens a native Pixel Bot window.

### Command-line options

```
uv run pixelbot --help

  --no-gui          Run backend only. Open http://localhost:<port> in any browser.
  --port <N>        Preferred port (a nearby free one is picked if <N> is taken).
  --debug           Verbose logs.
```

## Usage

1. Click **Add Monitor**.
2. Pick a pixel with the desktop overlay.
3. Choose a monitor type (Normal / Master / Slave) and trigger mode (Match / No-match).
4. Assign an action (keypress, hotkey, or log).
5. Monitor starts firing immediately.

### Monitor types

| Type | Behaviour |
|------|-----------|
| Normal | Independent. Fires when its condition holds. |
| Master | Checks up to 6 pixels with AND/OR logic. Gates its slaves. |
| Slave  | Only fires while its master is active. Useful for "UI visible" gates. |

## Project layout

```
pixelbot/              # Launcher package (entry point, PyWebView)
    __main__.py
    launcher.py
backend/               # Flask + SocketIO server and business logic
    app.py
    config.py  config_loader.py
    pixel_monitor.py   desktop_picker.py
    bot/               # Screen capture + pixel detection
    models/            # Data models
    services/          # Monitor logic + persistence
    routes/            # HTTP API
    websocket/         # Socket.IO events
    static/            # Vue 3 (CDN) frontend
PixelBot.spec          # PyInstaller config
build.ps1              # Build a single-file .exe (uv + PyInstaller)
start.ps1 / start.bat  # Run the app via uv
pyproject.toml         # Deps, entry points, build config
```

## Building a standalone `.exe`

```powershell
.\build.ps1
# -> dist\PixelBot.exe
```

The resulting executable bundles Python and all deps. Distribute the single `.exe` — no Python or uv needed on the target machine.

## Configuration (optional)

Drop a `pixelbot_config.ini` next to `PixelBot.exe` to override defaults:

```ini
[server]
port = 5000
host = 0.0.0.0

[monitoring]
check_interval = 0.1
default_tolerance = 10
default_cooldown = 1000

[advanced]
log_level = INFO
picker_timeout = 30
```

## Troubleshooting

- **Port already in use** — Pixel Bot automatically picks the next free port. Check the console for the chosen one.
- **Actions don't land in the game** — Run as Administrator, and use borderless windowed mode (not exclusive fullscreen).
- **Monitor won't trigger** — Re-pick the pixel (your UI may have shifted) or increase tolerance.
- **Native window doesn't open** — The launcher will fall back to opening your default browser. Use `--no-gui` to skip the window entirely.
- **Antivirus false positive on the built `.exe`** — Common for PyInstaller bundles. Whitelist it or build from source.

## Tech stack

| Layer | Tooling |
|---|---|
| Runtime | Python 3.10+, uv |
| Backend | Flask, Flask-SocketIO, MSS, NumPy, Pillow, PyAutoGUI |
| Desktop shell | PyWebView |
| Frontend | Vue 3 (CDN), Socket.IO client |
| Build | PyInstaller |

## License

MIT — see [LICENSE](LICENSE).

## Legal notice

Always check your game's Terms of Service before using automation. Some games prohibit it. Use at your own risk.
