"""
Pixel Bot Application - Main Flask Server (Refactored)
A pixel bot for screen capture, pixel detection, and automation
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import logging
import sys

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
    # Create necessary directories
    os.makedirs(Config.STATIC_FOLDER, exist_ok=True)
    
    # Find a free port if the default is in use
    try:
        port = Config.find_free_port(Config.PORT, max_attempts=10)
        if port != Config.PORT:
            logger.warning(f"Port {Config.PORT} is in use. Using port {port} instead.")
            Config.PORT = port
    except Exception as e:
        logger.error(f"Error finding free port: {e}")
        # Fall back to default port
        port = Config.PORT
    
    # Load monitors from file on startup
    monitors = persistence_service.load_monitors()
    monitor_service.load_monitors(monitors)
    
    # Start monitoring if there are monitors
    if monitor_service.count() > 0:
        monitoring_loop.start()
    
    print('=' * 50)
    print('Pixel Bot Server Starting...')
    print(f'Server: http://localhost:{port}')
    print(f'Loaded {monitor_service.count()} monitor(s) from config')
    counts = monitor_service.count_by_type()
    print(f'  - Masters: {counts["master"]}, Slaves: {counts["slave"]}, Normal: {counts["normal"]}')
    print('=' * 50)
    
    # Auto-open browser if running as standalone
    is_standalone = getattr(sys, 'frozen', False)
    if is_standalone:
        import webbrowser
        import threading
        def open_browser():
            import time
            time.sleep(2)  # Wait for server to start
            webbrowser.open(f'http://localhost:{port}')
        threading.Thread(target=open_browser, daemon=True).start()
        logger.info("Running as standalone - browser will open automatically")
    
    # Run the Flask-SocketIO server
    try:
        socketio.run(app, debug=Config.DEBUG, host=Config.HOST, port=port)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {port} is already in use. Please close other instances or specify a different port.")
            print("\n" + "="*50)
            print(f"ERROR: Port {port} is already in use!")
            print("Please close other instances of Pixel Bot or change the port in config.")
            print("="*50)
            input("Press Enter to exit...")
        else:
            raise
