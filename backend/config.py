"""
Configuration settings for Pixel Bot Application
"""
import os
import socket

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS settings
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*')
    
    # File paths
    STATIC_FOLDER = 'static'
    MONITORS_FILE = os.getenv('MONITORS_FILE', 'monitors_config.json')
    
    # Monitoring settings
    MONITOR_CHECK_INTERVAL = float(os.getenv('MONITOR_CHECK_INTERVAL', 0.1))  # 10 times per second
    DEFAULT_TOLERANCE = int(os.getenv('DEFAULT_TOLERANCE', 10))
    DEFAULT_COOLDOWN = int(os.getenv('DEFAULT_COOLDOWN', 1000))  # milliseconds
    PICKER_TIMEOUT = int(os.getenv('PICKER_TIMEOUT', 30))  # seconds
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Default monitor settings
    MONITOR_DEFAULTS = {
        'tolerance': DEFAULT_TOLERANCE,
        'cooldown': DEFAULT_COOLDOWN,
        'enabled': True,
        'monitor_type': 'normal',
        'master_id': None,
        'trigger_mode': 'no_match',
        'pixel_group': [],
        'group_logic': 'all_match',
        'last_trigger_time': 0,
        'in_cooldown': False,
        'blocked_by_master': False,
        'match_count': 0,
        'last_match': None
    }
    
    @staticmethod
    def find_free_port(start_port=5000, max_attempts=10):
        """
        Find a free port starting from start_port
        
        Args:
            start_port: Port to start checking from
            max_attempts: Maximum number of ports to try
        
        Returns:
            Free port number
        """
        for port in range(start_port, start_port + max_attempts):
            try:
                # Try to bind to the port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    s.close()
                    return port
            except OSError:
                # Port is in use, try next one
                continue
        
        # If no port found in range, return a random high port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to any free port
            port = s.getsockname()[1]
            s.close()
            return port


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'


# Config selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

