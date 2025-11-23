"""
Configuration loader for INI file
"""
import os
import configparser
import logging

logger = logging.getLogger(__name__)

def load_config_from_ini(config_class):
    """
    Load configuration from pixelbot_config.ini if it exists
    
    Args:
        config_class: The Config class to update
    """
    # Check for config file in current directory or executable directory
    config_paths = [
        'pixelbot_config.ini',  # Current directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pixelbot_config.ini'),  # Backend dir
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pixelbot_config.ini'),  # Project root
    ]
    
    # If running as standalone, check next to exe
    import sys
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        config_paths.insert(0, os.path.join(exe_dir, 'pixelbot_config.ini'))
    
    config_file = None
    for path in config_paths:
        if os.path.exists(path):
            config_file = path
            break
    
    if not config_file:
        logger.info("No config file found. Using defaults.")
        return
    
    try:
        parser = configparser.ConfigParser()
        parser.read(config_file)
        
        logger.info(f"Loading configuration from {config_file}")
        
        # Server settings
        if parser.has_section('server'):
            if parser.has_option('server', 'port'):
                config_class.PORT = parser.getint('server', 'port')
                logger.info(f"Config: PORT = {config_class.PORT}")
            if parser.has_option('server', 'host'):
                config_class.HOST = parser.get('server', 'host')
                logger.info(f"Config: HOST = {config_class.HOST}")
        
        # Monitoring settings
        if parser.has_section('monitoring'):
            if parser.has_option('monitoring', 'check_interval'):
                config_class.MONITOR_CHECK_INTERVAL = parser.getfloat('monitoring', 'check_interval')
                logger.info(f"Config: MONITOR_CHECK_INTERVAL = {config_class.MONITOR_CHECK_INTERVAL}")
            if parser.has_option('monitoring', 'default_tolerance'):
                config_class.DEFAULT_TOLERANCE = parser.getint('monitoring', 'default_tolerance')
                logger.info(f"Config: DEFAULT_TOLERANCE = {config_class.DEFAULT_TOLERANCE}")
            if parser.has_option('monitoring', 'default_cooldown'):
                config_class.DEFAULT_COOLDOWN = parser.getint('monitoring', 'default_cooldown')
                logger.info(f"Config: DEFAULT_COOLDOWN = {config_class.DEFAULT_COOLDOWN}")
        
        # Advanced settings
        if parser.has_section('advanced'):
            if parser.has_option('advanced', 'log_level'):
                config_class.LOG_LEVEL = parser.get('advanced', 'log_level').upper()
                logger.info(f"Config: LOG_LEVEL = {config_class.LOG_LEVEL}")
            if parser.has_option('advanced', 'picker_timeout'):
                config_class.PICKER_TIMEOUT = parser.getint('advanced', 'picker_timeout')
                logger.info(f"Config: PICKER_TIMEOUT = {config_class.PICKER_TIMEOUT}")
        
        logger.info("Configuration loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        logger.info("Falling back to default configuration")

