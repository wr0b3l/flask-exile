"""
Pixel Bot Application - Main Flask Server (Refactored)
A pixel bot for screen capture, pixel detection, and automation
"""

import logging

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

# Import configuration
from config import get_config
from config_loader import load_config_from_ini

# Import services
from services import MonitorService, PersistenceService, MonitoringLoop

# Import routes
from routes.monitor_routes import init_monitor_routes
from routes.pixel_routes import init_pixel_routes
from routes.screen_routes import screen_bp
from routes.picker_routes import picker_bp

# Import websocket
from websocket import init_websocket_events

# Get configuration
Config = get_config()

# Load user config from INI file if exists
load_config_from_ini(Config)

# Setup logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app, origins=Config.CORS_ALLOWED_ORIGINS)
socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ALLOWED_ORIGINS)

# Bot state
bot_state = {
    'running': False,
    'mode': 'idle'
}

# Initialize services
monitor_service = MonitorService()
persistence_service = PersistenceService()
monitoring_loop = MonitoringLoop(monitor_service, socketio)

# Initialize and register routes
monitor_bp = init_monitor_routes(monitor_service, persistence_service, monitoring_loop, socketio)
pixel_bp = init_pixel_routes(socketio)

app.register_blueprint(monitor_bp)
app.register_blueprint(pixel_bp)
app.register_blueprint(screen_bp)
app.register_blueprint(picker_bp)

# Initialize WebSocket events
init_websocket_events(socketio, bot_state)


@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory(Config.STATIC_FOLDER, 'dashboard.html')


@app.route('/api/status')
def get_status():
    """Get current bot status"""
    from flask import jsonify
    return jsonify(bot_state)


if __name__ == '__main__':
    # Direct invocation (legacy). Prefer `uv run pixelbot` which uses the launcher.
    from pixelbot.launcher import run as _run  # type: ignore

    _run()
