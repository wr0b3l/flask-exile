"""Boots the Flask+SocketIO backend and (optionally) a PyWebView window.

The backend module lives under `backend/` with flat imports (`from services import ...`),
so we prepend it to sys.path rather than restructuring every import.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path

logger = logging.getLogger("pixelbot")


def _repo_root() -> Path:
    if getattr(sys, "frozen", False):
        # PyInstaller one-file: resources live in _MEIPASS
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent


def _prime_sys_path() -> Path:
    """Make `backend/` importable regardless of where we're invoked from."""
    backend = _repo_root() / "backend"
    if getattr(sys, "frozen", False):
        # In PyInstaller bundle, backend modules are flattened to _MEIPASS root
        backend = _repo_root()
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    return backend


def _start_flask(port_override: int | None, debug: bool) -> int:
    """Configure and start the Flask+SocketIO server. Returns the chosen port."""
    backend = _prime_sys_path()
    os.chdir(backend if not getattr(sys, "frozen", False) else _repo_root())

    # Imports deferred until sys.path is ready
    from app import Config, app, monitor_service, monitoring_loop, persistence_service, socketio  # type: ignore

    if debug:
        Config.DEBUG = True

    preferred = port_override or Config.PORT
    try:
        port = Config.find_free_port(preferred, max_attempts=10)
    except Exception:
        port = preferred
    Config.PORT = port

    monitors = persistence_service.load_monitors()
    monitor_service.load_monitors(monitors)
    if monitor_service.count() > 0:
        monitoring_loop.start()

    counts = monitor_service.count_by_type()
    print("=" * 50)
    print(f"Pixel Bot v{_version()} — http://localhost:{port}")
    print(
        f"Loaded {monitor_service.count()} monitor(s) "
        f"(masters: {counts['master']}, slaves: {counts['slave']}, normal: {counts['normal']})"
    )
    print("=" * 50)

    # Run the Socket.IO server in a daemon thread so the main thread can host PyWebView.
    def _serve() -> None:
        try:
            socketio.run(
                app,
                debug=False,  # never run werkzeug reloader from a thread
                host=Config.HOST,
                port=port,
                allow_unsafe_werkzeug=True,
            )
        except TypeError:
            # Older Flask-SocketIO doesn't accept allow_unsafe_werkzeug
            socketio.run(app, debug=False, host=Config.HOST, port=port)
        except OSError as e:
            logger.error("Server error: %s", e)

    threading.Thread(target=_serve, name="pixelbot-server", daemon=True).start()
    return port


def _run_webview(port: int) -> None:
    """Open a native window pointing at the running server."""
    import webview  # imported lazily so --no-gui installs without GUI deps resolved

    url = f"http://localhost:{port}"
    webview.create_window(
        title="Pixel Bot",
        url=url,
        width=1280,
        height=860,
        min_size=(960, 640),
        background_color="#1a1410",
    )
    webview.start()


def _run_fallback_browser(port: int) -> None:
    """Open the default browser and block until Ctrl+C."""
    import time
    import webbrowser

    webbrowser.open(f"http://localhost:{port}")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nStopping Pixel Bot.")


def _version() -> str:
    try:
        from importlib.metadata import version

        return version("pixelbot")
    except Exception:
        return "dev"


def run(no_gui: bool = False, port: int | None = None, debug: bool = False) -> int:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    chosen_port = _start_flask(port_override=port, debug=debug)

    if no_gui:
        print("Running in --no-gui mode. Press Ctrl+C to quit.")
        _run_fallback_browser(chosen_port)
        return 0

    try:
        _run_webview(chosen_port)
    except Exception as e:
        logger.warning("Native window unavailable (%s); falling back to browser.", e)
        _run_fallback_browser(chosen_port)
    return 0
