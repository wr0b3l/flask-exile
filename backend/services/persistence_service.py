"""
Persistence Service - Handle saving and loading monitors
"""
import json
import os
import logging
from typing import List, Dict, Any
from config import Config

logger = logging.getLogger(__name__)


class PersistenceService:
    """Service for loading and saving monitor configurations"""
    
    def __init__(self, file_path: str = None):
        """
        Initialize persistence service
        
        Args:
            file_path: Path to monitors config file (defaults to Config.MONITORS_FILE)
        """
        self.file_path = file_path or Config.MONITORS_FILE
    
    def load_monitors(self) -> List[Dict[str, Any]]:
        """
        Load monitors from JSON file
        
        Returns:
            List of monitor dictionaries
        """
        try:
            if not os.path.exists(self.file_path):
                logger.info(f"No monitors file found at {self.file_path}")
                return []
            
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                monitors = data.get('monitors', [])
                
                # Ensure all monitors have required fields with defaults
                for monitor in monitors:
                    for key, default_value in Config.MONITOR_DEFAULTS.items():
                        if key not in monitor:
                            monitor[key] = default_value
                    
                    # Log the loaded state
                    pixel_count = 1 + len(monitor.get('pixel_group', []))
                    logger.info(
                        f"Loaded monitor '{monitor['name']}' (ID: {monitor['id']}) "
                        f"- type: {monitor['monitor_type']}, enabled: {monitor['enabled']}, "
                        f"pixels: {pixel_count}"
                    )
                
                logger.info(f"Successfully loaded {len(monitors)} monitors from {self.file_path}")
                return monitors
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from {self.file_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading monitors from file: {e}")
            return []
    
    def save_monitors(self, monitors: List[Dict[str, Any]]) -> bool:
        """
        Save monitors to JSON file
        
        Args:
            monitors: List of monitor dictionaries
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a clean copy for JSON serialization (remove runtime-only fields)
            monitors_to_save = []
            for monitor in monitors:
                clean_monitor = {
                    'id': monitor['id'],
                    'name': monitor['name'],
                    'x': monitor['x'],
                    'y': monitor['y'],
                    'target_color': monitor['target_color'],
                    'tolerance': monitor.get('tolerance', Config.DEFAULT_TOLERANCE),
                    'cooldown': monitor.get('cooldown', Config.DEFAULT_COOLDOWN),
                    'action': monitor['action'],
                    'enabled': monitor['enabled'],
                    'monitor_type': monitor.get('monitor_type', 'normal'),
                    'master_id': monitor.get('master_id', None),
                    'trigger_mode': monitor.get('trigger_mode', 'no_match'),
                    'pixel_group': monitor.get('pixel_group', []),
                    'group_logic': monitor.get('group_logic', 'all_match')
                }
                monitors_to_save.append(clean_monitor)
            
            import time
            data = {
                'monitors': monitors_to_save,
                'saved_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(monitors)} monitors to {self.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving monitors to file: {e}")
            return False

