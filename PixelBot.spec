# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Pixel Bot (single-file Windows build).

Entry point: the thin `pixelbot` package which boots Flask+SocketIO and
opens a PyWebView window pointing at the local server.
"""

block_cipher = None


a = Analysis(
    ['pixelbot/__main__.py'],
    pathex=['backend'],
    binaries=[],
    datas=[
        # Static frontend assets
        ('backend/static', 'static'),

        # Backend Python modules (flat-imported from backend/)
        ('backend/config.py', '.'),
        ('backend/config_loader.py', '.'),
        ('backend/app.py', '.'),
        ('backend/pixel_monitor.py', '.'),
        ('backend/desktop_picker.py', '.'),
        ('backend/models', 'models'),
        ('backend/services', 'services'),
        ('backend/routes', 'routes'),
        ('backend/websocket', 'websocket'),
        ('backend/bot', 'bot'),

        # Example config
        ('backend/pixelbot_config.example.ini', '.'),
    ],
    hiddenimports=[
        # Flask + extensions
        'flask',
        'flask_socketio',
        'flask_cors',
        'werkzeug',
        'jinja2',

        # SocketIO transports
        'engineio.async_drivers.threading',
        'socketio',
        'engineio',
        'simple_websocket',

        # Screen capture + automation
        'mss',
        'mss.windows',
        'PIL',
        'PIL._tkinter_finder',
        'pyautogui',
        'numpy',

        # Native window
        'webview',
        'webview.platforms.winforms',

        # Standard library bits PyInstaller sometimes misses
        'tkinter',
        'configparser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Things we definitely don't ship
        'matplotlib',
        'pandas',
        'scipy',
        'pytest',
        'IPython',
        'cv2',
        'pytesseract',
        'pynput',
        'requests',
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # native PyWebView window — no terminal needed
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='backend/static/images/logo.png',
    version_file=None,
)
