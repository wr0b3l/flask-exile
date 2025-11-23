# Pixel Bot - Desktop Automation Tool

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A powerful desktop automation tool for Windows that monitors screen pixels and triggers keyboard actions. Perfect for gaming automation, workflow automation, and repetitive tasks.

![Pixel Bot Dashboard](backend/static/images/logo.png)

## ✨ Features

### Core Functionality
- 🎯 **Pixel Monitoring** - Monitor specific screen pixels with color tolerance
- 🔍 **Desktop Pixel Picker** - System-wide overlay for accurate pixel selection
- ⌨️ **Input Automation** - Trigger keyboard actions (keypresses, hotkeys)
- 📊 **Real-time Dashboard** - Vue.js-powered web interface with live updates
- 💾 **Persistent Configuration** - Save and load monitor setups

### Advanced Features
- 👑 **Master-Slave System** - Hierarchical monitoring to handle loading screens
- 🔢 **Multi-Pixel Detection** - Check up to 6 pixels with AND/OR logic (master monitors)
- ⏱️ **Cooldown System** - Prevent action spam with configurable delays
- 🎨 **Custom Dark Theme** - Path of Exile 2 inspired UI
- 🔌 **Smart Port Detection** - Auto-finds free ports (5000-5009)
- ⚙️ **INI Configuration** - Optional user configuration file

### Distribution
- 📦 **Standalone Executable** - PyInstaller builds for easy distribution
- 🚀 **No Dependencies** - Works on any Windows PC without Python
- 🔧 **Professional Installer** - Inno Setup scripts included

## 🚀 Quick Start

### For Users (Standalone)

1. **Download** the latest release from [Releases](https://github.com/wr0b3l/flask-exile/releases)
2. **Run** `PixelBot.exe`
3. **Browser opens** automatically with the dashboard
4. **Create monitors** and start automating!

No Python or setup required! ✨

### For Developers

#### Prerequisites
- Python 3.11+
- Windows 10/11
- Git

#### Installation

```bash
# Clone the repository
git clone https://github.com/wr0b3l/flask-exile.git
cd flask-exile

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend\requirements.txt

# Run the application
cd backend
python app.py
```

The dashboard will open at `http://localhost:5000`

## 📖 Usage

### Creating a Monitor

1. **Click "Add Monitor"** in the dashboard
2. **Basic Info Tab:**
   - Enter a name (e.g., "Health Low Alert")
   - Set color tolerance (default: 10)

3. **Pixels Tab:**
   - Click "Pick Pixel from Screen"
   - Click on the pixel you want to monitor
   - Add more pixels for multi-pixel checks (masters only)

4. **Type & Mode Tab:**
   - Choose monitor type (Normal/Master/Slave)
   - Set trigger mode (Match/No Match)

5. **Action Tab:**
   - Select action type (Key Press/Hotkey/Log Only)
   - Enter the key (e.g., "r", "ctrl+1")
   - Set cooldown (milliseconds)

6. **Click "Add Monitor"**

### Monitor Types

#### Normal Monitor
- Independent pixel monitoring
- Triggers action when condition is met
- Simple and straightforward

#### Master Monitor
- Can check multiple pixels (up to 6)
- Controls linked "slave" monitors
- When master is ACTIVE → slaves can run
- When master is INACTIVE → slaves are blocked

**Use case:** Check if game UI is visible (multiple UI elements)

#### Slave Monitor
- Linked to a master monitor
- Only runs when master is active
- Prevents false triggers during loading screens

**Use case:** Health monitoring (only when UI is visible)

### Trigger Modes

- **Match** - Triggers when pixel IS the target color
- **No Match** - Triggers when pixel is NOT the target color

## 🏗️ Architecture

### Backend (Python)
- **Framework:** Flask + Flask-SocketIO
- **Modular Design:** Config, Models, Services, Routes, WebSocket
- **Monitoring:** Background thread (100ms interval)
- **Libraries:** MSS (screen capture), PyAutoGUI (input), Pynput (control)

### Frontend (Vue.js 3 CDN)
- **Framework:** Vue.js 3 (no build step required)
- **Components:** Modular, reusable components
- **Services:** Centralized API and Socket.IO
- **Theme:** Custom dark theme with pulsing logo

### Project Structure

```
flask-exile/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration with port detection
│   ├── config_loader.py    # INI file loader
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── routes/             # API endpoints
│   ├── websocket/          # Socket.IO events
│   ├── bot/                # Automation modules
│   └── static/             # Vue.js dashboard
├── PixelBot.spec          # PyInstaller configuration
├── build_standalone.ps1   # Build script for .exe
├── build_installer.ps1    # Installer build script
└── requirements-build.txt # Build dependencies
```

## 🛠️ Building Standalone Executable

### Build the .exe

```powershell
# Install build tools
pip install -r requirements-build.txt

# Build standalone executable
.\build_standalone.ps1 -Clean

# Output: dist/PixelBot.exe (~67 MB)
```

### Create Installer (Optional)

Requires [Inno Setup](https://jrsoftware.org/isinfo.php)

```powershell
.\build_installer.ps1

# Output: installer/PixelBot_Setup_v1.0.0.exe
```

## ⚙️ Configuration

### Optional Config File

Create `pixelbot_config.ini` next to `PixelBot.exe`:

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

## 📊 Performance

- **CPU Usage:** ~0.5-1% on modern CPUs
- **Memory:** ~70 MB
- **Check Frequency:** 10 times per second (100ms interval)
- **Response Time:** 6-18ms (detection + action)
- **Max Monitors:** 20-30 before optimization needed

## 🐛 Troubleshooting

### Port Already in Use
- **Auto-handled!** App finds next free port automatically
- Check console for actual port being used

### Monitor Not Triggering
- Re-pick the pixel (screen may have changed)
- Increase tolerance (try 15-20)
- Check trigger mode (Match vs No Match)
- Verify cooldown isn't blocking

### Actions Not Working
- Run as Administrator if needed
- Use borderless windowed mode (not fullscreen)
- Check key name spelling

### Antivirus False Positive
- Common with PyInstaller executables
- Add to whitelist or use code signing

## 📝 Development

### Tech Stack

**Backend:**
- Python 3.13
- Flask 2.3
- Flask-SocketIO 5.3
- MSS 9.0 (screen capture)
- NumPy 2.1 (pixel operations)
- OpenCV 4.12 (image processing)
- PyAutoGUI 0.9 (automation)
- Pynput 1.7 (input control)

**Frontend:**
- Vue.js 3.5 (CDN)
- Socket.IO Client
- Custom CSS (Path of Exile 2 theme)

**Build:**
- PyInstaller 6.16
- Inno Setup (optional)

### Running Tests

```bash
# Start development server
cd backend
python app.py

# Open browser
http://localhost:5000
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

**Important:** Always check your game's Terms of Service before using automation tools. Some games prohibit automation and may ban accounts.

**This tool is provided as-is with no warranty. Use at your own risk.**

## 🙏 Acknowledgments

- **Flask & Vue.js** - Excellent frameworks
- **PyInstaller** - Making Python distribution easy
- **Path of Exile 2** - UI design inspiration
- **MSS** - Fast screen capture library

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/wr0b3l/flask-exile/issues)
- **Discussions:** [GitHub Discussions](https://github.com/wr0b3l/flask-exile/discussions)
- **Documentation:** [User Guide](USER_GUIDE.md)

## 🗺️ Roadmap

- [ ] System tray icon (hide console)
- [ ] Keyboard shortcuts
- [ ] Monitor templates
- [ ] Export/import monitors
- [ ] Performance profiling UI
- [ ] Auto-update system
- [ ] Multi-language support

## 📈 Stats

- **Lines of Code:** ~9,000
- **Components:** 10+ Vue components
- **API Endpoints:** 20+
- **Build Time:** ~45 seconds
- **Executable Size:** ~67 MB

---

**Made with ❤️ for automation enthusiasts**

**Star ⭐ this repo if you find it useful!**
