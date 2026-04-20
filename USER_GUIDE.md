# Pixel Bot — User Guide

Pixel Bot watches specific pixels on your screen and fires keyboard actions when they change. Useful for Path of Exile (flasks, auto-loot triggers, UI-gated automation) and similar games or workflows.

---

## Running Pixel Bot

### Option A — Installed executable (end users)

1. Grab `PixelBot.exe` from the latest release.
2. Double-click it.
3. A **native Pixel Bot window** opens — no browser tab, no console.
4. Start adding monitors.

Your saved monitors live in `monitors_config.json` next to the `.exe` (created automatically).

### Option B — Run from source (developers)

Pixel Bot uses [uv](https://docs.astral.sh/uv/) for dependency management. uv fetches the right Python for you, so **you don't need Python on PATH**.

```powershell
# One-time: install uv
irm https://astral.sh/uv/install.ps1 | iex

# Run (from the repo root)
.\start.ps1
# or just double-click start.bat
```

First launch does a `uv sync` (downloads deps into `.venv/`). Subsequent launches are instant.

### Command-line flags

```
uv run pixelbot --help

  --no-gui          Run the backend only; open http://localhost:<port> in any browser.
  --port <N>        Preferred port. A nearby free port is picked if <N> is taken.
  --debug           Verbose logs.
```

---

## First monitor in 60 seconds

1. Click **Add Monitor**.
2. Give it a name (e.g. *"HP low"*).
3. Open the **Pixels** tab → **Pick Pixel from Screen** → click the pixel you want to watch. Coordinates and colour are captured automatically.
4. Open the **Type & Mode** tab → leave as **Normal** + **No Match** (fires when the pixel is no longer the target colour).
5. Open the **Action** tab → **Key Press** → type `1` (for example) → set cooldown `1000` ms.
6. Save. The monitor starts immediately.

---

## Monitor types

| Type | What it does |
|---|---|
| **Normal** | Checks one pixel. Fires when its condition holds. |
| **Master** | Checks **up to 6** pixels with `All Match` or `Any Match` logic. Gates its slaves. |
| **Slave**  | Linked to a master. Only fires while that master is active. Blocks loading-screen misfires. |

### Trigger modes

- **Match** — fire when the pixel **is** the target colour.
- **No Match** — fire when the pixel **is not** the target colour.

### Actions

- **Key Press** — single key (`r`, `1`, `F1`, `space`).
- **Hotkey** — combo (`ctrl+1`, `shift+f`).
- **Log Only** — no action; useful for dry-running a new monitor.

---

## Patterns that tend to work well

### Health/mana flask

```
Type:     Normal
Pixel:    a point inside your HP bar at the threshold you want
Trigger:  No Match (fires when the HP pixel leaves its "healthy" colour)
Action:   Key Press "1"
Cooldown: 4000–6000 ms (match the flask charge regen)
```

### Loading-screen gate

```
Master:
  Name:    "UI visible"
  Pixels:  2–3 points that only exist on the HUD (map icon, flask frames...)
  Logic:   All Match
  Action:  Log Only

All your gameplay monitors → set type = Slave, master = "UI visible".
```

Now nothing fires during loading screens, vendor windows, or cutscenes.

---

## Tips

- Start any new monitor as **Log Only** — confirm it fires at the right moments before wiring up an action.
- Increase **tolerance** (15–25) if colours vary with lighting/animations.
- Don't monitor pixels inside gradients or animated elements.
- Keep cooldowns honest — too low and you'll spam actions faster than your flasks recharge.
- Use descriptive names. You'll forget what `Monitor_3` was.

---

## Configuration (optional)

Drop `pixelbot_config.ini` next to `PixelBot.exe` (or the project root when running from source):

```ini
[server]
port = 5000
host = 0.0.0.0

[monitoring]
check_interval = 0.1       ; 0.1 = 10 checks/sec. Lower = faster & more CPU.
default_tolerance = 10     ; 0–255. Higher = more lenient colour matching.
default_cooldown = 1000    ; ms between fires for new monitors.

[advanced]
log_level = INFO           ; DEBUG / INFO / WARNING / ERROR
picker_timeout = 30        ; seconds before the pixel picker gives up
```

---

## Troubleshooting

**Native window doesn't open.**
The launcher falls back to opening your default browser at `http://localhost:<port>`. You can also run with `--no-gui` to skip the window entirely.

**"Port already in use".**
Pixel Bot hunts for the next free port automatically. Check the log line at startup (`Pixel Bot vX.Y — http://localhost:5001`).

**Monitor won't trigger.**
- Re-pick the pixel. Your HUD may have shifted (resolution change, new layout).
- Increase tolerance.
- Check trigger mode — Match vs No Match are easy to flip.
- If it's a slave, verify its master is active.

**Actions don't reach the game.**
- Run Pixel Bot **as Administrator** — many games require elevated processes to receive synthetic input.
- Use **borderless windowed** mode, not exclusive fullscreen.
- Double-check the key name spelling.

**Pixel picker overlay is invisible / stuck.**
- Close other overlays (Discord, NVIDIA overlay, Steam overlay) that might capture mouse input first.
- Run as Administrator.

**Antivirus flags the built `.exe`.**
Common PyInstaller false positive. Whitelist the executable, or build it yourself from source with `.\build.ps1`.

**Game has anti-cheat.**
Some games actively block synthetic input or flag automation. Check the game's ToS before using Pixel Bot; use at your own risk.

---

## FAQ

**Can I run multiple instances?**
Yes. Each one auto-picks a free port.

**Where are my monitors saved?**
`monitors_config.json`, in the same folder as `PixelBot.exe` (or the project root in dev mode).

**How do I back them up?**
Copy `monitors_config.json` somewhere safe.

**How do I stop it?**
Close the Pixel Bot window. In `--no-gui` mode, press `Ctrl+C` in the terminal.

**Does OCR work?**
OCR and image-template matching were removed in v1.1 — they weren't wired to the UI, and `pytesseract`/`opencv` added ~200 MB to the build for nothing. Open an issue if you actually need them.

---

## Legal

Always check the Terms of Service of the game or application before using automation. Some games prohibit it, and accounts have been banned. Pixel Bot is provided as-is, with no warranty.
