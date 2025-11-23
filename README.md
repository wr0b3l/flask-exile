# Pixel Bot - Automated Pixel Detection & Monitoring

A powerful desktop automation tool for pixel detection, continuous monitoring, and automated actions.

## 🎯 Features

- **System-Wide Pixel Picking**: Pick pixels from anywhere on your screen (any app, game, or desktop)
- **Continuous Monitoring**: Monitor multiple pixels simultaneously for color changes
- **Automated Actions**: Trigger keyboard/mouse actions when pixel colors match
- **Web Dashboard**: Beautiful control panel for managing monitors and viewing statistics
- **Real-Time Updates**: Live activity log via WebSocket
- **Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- All dependencies installed

### Installation

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Start the application:**
```bash
.\start-dev.ps1
```

3. **Open dashboard:**
```
http://localhost:5000
```

## 📖 Usage

### Method 1: Web Dashboard (Recommended)

1. Open http://localhost:5000
2. Click "Pick Pixel" to launch desktop overlay
3. Click anywhere on screen to select pixel
4. Add monitors and configure actions
5. View real-time updates

### Method 2: Command Line

**Pick a pixel:**
```bash
cd backend
python desktop_picker.py --pick
```

**Monitor a pixel:**
```bash
cd backend
python desktop_picker.py --monitor 100 100 --color 255 0 0 --key space
```

**Advanced monitoring:**
```python
import sys
sys.path.append('backend')
from pixel_monitor import PixelMonitor

monitor = PixelMonitor()
monitor.add_monitor(
    x=100, y=50,
    target_color=(255, 0, 0),
    action={'type': 'keypress', 'key': 'h'},
    name="Health Monitor"
)
monitor.run()
```

## 📁 Project Structure

```
potta/
├── backend/
│   ├── app.py                    # Flask API server + WebSocket
│   ├── desktop_picker.py         # Desktop pixel picker overlay
│   ├── pixel_monitor.py          # Pixel monitoring system
│   ├── bot/
│   │   ├── screen_capture.py    # Screen capture
│   │   ├── pixel_detector.py    # Pixel detection
│   │   ├── image_matcher.py     # Image matching
│   │   └── text_reader.py       # OCR (requires Tesseract)
│   ├── static/
│   │   └── dashboard.html        # Web dashboard (single file)
│   ├── requirements.txt
│   └── venv/
├── start-dev.ps1                 # Launch script (Windows)
├── start-dev.py                  # Launch script (cross-platform)
└── README.md                     # This file
```

## 🎮 Use Cases

### Game Automation
```python
# Monitor health bar, use potion when low
monitor.add_monitor(
    x=100, y=50,
    target_color=(255, 0, 0),  # Red = low health
    action={'type': 'keypress', 'key': 'h'}
)
```

### UI Testing
```python
# Wait for button to become enabled (green)
monitor.add_monitor(
    x=500, y=300,
    target_color=(0, 255, 0),  # Green = enabled
    action={'type': 'click', 'x': 500, 'y': 300}
)
```

### Screen Monitoring
```python
# Alert when specific color appears
monitor.add_monitor(
    x=800, y=600,
    target_color=(255, 255, 0),  # Yellow alert
    action={'type': 'log'}
)
```

## 🔧 Configuration

### Pixel Monitor Actions

**Keypress:**
```python
action={'type': 'keypress', 'key': 'space'}
```

**Hotkey Combo:**
```python
action={'type': 'hotkey', 'keys': ['ctrl', 'c']}
```

**Mouse Click:**
```python
action={'type': 'click', 'x': 500, 'y': 300, 'button': 'left'}
```

**Custom Callback:**
```python
def my_callback(monitor, color):
    print(f"Matched! Color: {color}")

action={'type': 'callback', 'function': my_callback}
```

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web dashboard |
| `/api/status` | GET | Server status |
| `/api/screen/capture` | POST | Capture screenshot |
| `/api/pixel/get-color` | POST | Get pixel color |
| `/api/picker/launch` | POST | Launch desktop pixel picker |
| `/api/monitor/add` | POST | Add pixel monitor |
| `/api/monitor/list` | GET | List monitors |
| `/api/monitor/remove/<id>` | DELETE | Remove monitor |
| `/api/monitor/toggle/<id>` | POST | Pause/resume monitor |
| `/api/monitor/edit/<id>` | PUT | Edit monitor settings |

## 🔌 WebSocket Events

- `connect` - Client connected
- `monitor_update` - Monitor list updated
- `monitor_match` - Pixel color matched
- `action_triggered` - Action executed

## 📊 Technical Details

### Technologies
- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript, Socket.IO
- **Automation**: PyAutoGUI, Tkinter
- **Vision**: MSS, OpenCV, Pillow, Tesseract

### Performance
- Screen capture: ~20-30ms (4K)
- Pixel detection: ~5-10ms
- Monitor checks: 10/second (configurable)

## 🐛 Troubleshooting

**Port already in use:**
```bash
.\kill-ports.ps1
```

**Threading errors:**
- Fixed! Each request creates fresh MSS instance

**Wrong pixel colors:**
- Use desktop_picker.py instead of browser picking

**Tesseract not found:**
- Install from: https://github.com/UB-Mannheim/tesseract/wiki
- Configure path in `backend/bot/text_reader.py`

## 📝 Documentation

- `README.md` - This file (main documentation)
- `ARCHITECTURE.md` - System architecture and design
- `ARCHITECTURAL_REDESIGN.txt` - Major design decisions
- `SIMPLIFIED_ARCHITECTURE.txt` - Final architecture explanation

## 🎉 Quick Tips

1. **Pick pixels accurately**: Use desktop_picker.py for system-wide picking
2. **Monitor multiple pixels**: Add as many monitors as needed
3. **Adjust tolerance**: Increase for similar colors, decrease for exact matches
4. **Save configurations**: Use `monitor.save_config('myconfig.json')`
5. **View logs**: Check activity log in web dashboard

## 🚦 Getting Started

```bash
# 1. Start the server
.\start-dev.ps1

# 2. Open dashboard
# http://localhost:5000

# 3. Click "Pick Pixel"
# Desktop overlay appears

# 4. Click anywhere to select pixel

# 5. Configure monitor and action

# 6. Watch it work!
```

## 📄 License

MIT License - Feel free to use for personal or commercial projects

## 🙏 Acknowledgments

Built with: Flask, PyAutoGUI, OpenCV, MSS, Tkinter, Socket.IO

---

**Status**: ✅ Production Ready

**Version**: 2.0.0 (Desktop-focused architecture)

**Last Updated**: November 2025
