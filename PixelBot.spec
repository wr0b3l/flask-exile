# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pixel Bot
Builds a standalone Windows executable with all dependencies
"""

import sys
from pathlib import Path

block_cipher = None

# Determine paths
backend_path = Path('backend')
bot_path = backend_path / 'bot'

a = Analysis(
    ['backend/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Static files (dashboard, CSS, JS, images)
        ('backend/static', 'static'),
        
        # Python modules
        ('backend/config.py', '.'),
        ('backend/config_loader.py', '.'),
        ('backend/models', 'models'),
        ('backend/services', 'services'),
        ('backend/routes', 'routes'),
        ('backend/websocket', 'websocket'),
        
        # Bot modules
        ('backend/bot', 'bot'),
        
        # Desktop picker script
        ('backend/desktop_picker.py', '.'),
        ('backend/pixel_monitor.py', '.'),
        
        # Config example file
        ('backend/pixelbot_config.example.ini', '.'),
    ],
    hiddenimports=[
        # Flask and extensions
        'flask',
        'flask_socketio',
        'flask_cors',
        'werkzeug',
        'jinja2',
        
        # SocketIO dependencies
        'engineio.async_drivers.threading',
        'socketio',
        'engineio',
        'simple_websocket',
        
        # Screen capture and automation
        'mss',
        'mss.windows',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'pyautogui',
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        
        # Computer vision - explicit imports for numpy and cv2
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        'numpy.core._multiarray_umath',
        'numpy.core._methods',
        'numpy.lib',
        'numpy.lib.format',
        'numpy.random',
        'cv2',
        
        # OCR (optional)
        'pytesseract',
        
        # Standard library
        'tkinter',
        'configparser',
        'logging',
        'json',
        'threading',
        'socket',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unused modules to reduce size
        'matplotlib',
        'pandas',
        'scipy',
        'pytest',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PixelBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for logs (set to False for no console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='backend/static/images/logo.png',  # Will try to use as icon
    version_file=None,
)

# Note: To hide console window, change console=True to console=False above
# For production, you may want console=False and use system tray instead

