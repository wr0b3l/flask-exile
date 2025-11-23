# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-23

### Added
- Initial release of Pixel Bot
- Pixel monitoring with color tolerance detection
- Desktop pixel picker overlay for system-wide pixel selection
- Master-slave monitor hierarchy system
- Multi-pixel checking (up to 6 pixels) with AND/OR logic for master monitors
- Real-time WebSocket dashboard with Vue.js 3
- Smart port auto-detection (5000-5009, then random)
- INI configuration file support
- Cooldown system to prevent action spam
- Activity logging with real-time updates
- Monitor persistence (save/load from JSON)
- PyInstaller build scripts for standalone Windows executable
- Inno Setup scripts for professional installer
- Tabbed monitor modal for better UX
- Shared Vue.js components for consistency
- Custom dark theme inspired by Path of Exile 2
- Comprehensive user guide and documentation

### Features
- **Monitor Types:**
  - Normal monitors (independent pixel checking)
  - Master monitors (multi-pixel with slave control)
  - Slave monitors (dependent on master state)

- **Trigger Modes:**
  - Match (trigger when pixel IS target color)
  - No Match (trigger when pixel is NOT target color)

- **Actions:**
  - Single key press
  - Hotkey combinations (e.g., ctrl+1)
  - Log only (for testing)

- **Configuration:**
  - Port configuration
  - Check interval customization
  - Default tolerance and cooldown settings
  - Log level control

### Technical
- Backend: Python 3.13, Flask 2.3, Flask-SocketIO 5.3
- Frontend: Vue.js 3.5 (CDN), custom CSS
- Automation: MSS 9.0, NumPy 2.1, OpenCV 4.12, PyAutoGUI 0.9, Pynput 1.7
- Build: PyInstaller 6.16
- Architecture: Modular design (config, models, services, routes, websocket)

### Performance
- CPU Usage: ~0.5-1% on modern CPUs
- Memory: ~70 MB
- Check Frequency: 10 times per second (100ms interval)
- Executable Size: ~67 MB (standalone)

### Known Issues
- Numpy was initially excluded from PyInstaller build (fixed)
- Tesseract OCR requires separate installation (optional feature)
- Some antivirus software may flag executable (false positive)

## [Unreleased]

### Planned
- System tray icon to hide console window
- Keyboard shortcuts for quick actions
- Monitor templates for common use cases
- Export/import monitor configurations
- Drag & drop monitor reordering
- Search/filter functionality for monitors
- Performance profiling UI
- Auto-update system
- Multi-language support (i18n)
- Cloud sync for monitor configurations
- Mobile dashboard (read-only)

---

[1.0.0]: https://github.com/wr0b3l/flask-exile/releases/tag/v1.0.0


