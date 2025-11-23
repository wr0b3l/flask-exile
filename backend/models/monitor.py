"""
Data models for Pixel Bot Application
"""
from typing import Dict, List, Optional, Any
from config import Config


class Monitor:
    """Monitor model with validation and helper methods"""
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize monitor from dictionary"""
        # Required fields
        self.id = data.get('id')
        self.name = data.get('name', f"Monitor {self.id}")
        self.x = data['x']
        self.y = data['y']
        self.target_color = data['target_color']  # [r, g, b]
        self.action = data['action']  # {type: 'keypress', key: 'space'}
        
        # Optional fields with defaults
        self.tolerance = data.get('tolerance', Config.DEFAULT_TOLERANCE)
        self.cooldown = data.get('cooldown', Config.DEFAULT_COOLDOWN)
        self.enabled = data.get('enabled', True)
        self.monitor_type = data.get('monitor_type', 'normal')  # 'normal', 'master', 'slave'
        self.master_id = data.get('master_id', None)
        self.trigger_mode = data.get('trigger_mode', 'no_match')  # 'match' or 'no_match'
        
        # Multi-pixel fields
        self.pixel_group = data.get('pixel_group', [])  # Additional pixels [{x, y, color, tolerance}]
        self.group_logic = data.get('group_logic', 'all_match')  # 'all_match' or 'any_match'
        
        # Runtime fields
        self.last_trigger_time = data.get('last_trigger_time', 0)
        self.in_cooldown = data.get('in_cooldown', False)
        self.blocked_by_master = data.get('blocked_by_master', False)
        self.match_count = data.get('match_count', 0)
        self.last_match = data.get('last_match', None)
        self._last_active_state = data.get('_last_active_state', None)
    
    def validate(self) -> Optional[str]:
        """
        Validate monitor data
        Returns: Error message if invalid, None if valid
        """
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            return "Invalid coordinates: x and y must be numbers"
        
        if not isinstance(self.target_color, list) or len(self.target_color) != 3:
            return "Invalid target_color: must be [r, g, b]"
        
        if not all(0 <= c <= 255 for c in self.target_color):
            return "Invalid target_color: RGB values must be 0-255"
        
        if self.tolerance < 0 or self.tolerance > 255:
            return "Invalid tolerance: must be 0-255"
        
        if self.cooldown < 0:
            return "Invalid cooldown: must be >= 0"
        
        if self.monitor_type not in ['normal', 'master', 'slave']:
            return "Invalid monitor_type: must be 'normal', 'master', or 'slave'"
        
        if self.monitor_type == 'slave' and not self.master_id:
            return "Slave monitors must have a master_id"
        
        if self.trigger_mode not in ['match', 'no_match']:
            return "Invalid trigger_mode: must be 'match' or 'no_match'"
        
        if self.group_logic not in ['all_match', 'any_match']:
            return "Invalid group_logic: must be 'all_match' or 'any_match'"
        
        # Multi-pixel is only allowed for master monitors
        if self.pixel_group and len(self.pixel_group) > 0:
            if self.monitor_type != 'master':
                return "Multi-pixel monitoring (pixel_group) is only available for master monitors"
        
        if not isinstance(self.action, dict) or 'type' not in self.action:
            return "Invalid action: must have 'type' field"
        
        # Validate pixel_group
        if self.pixel_group:
            for idx, pixel in enumerate(self.pixel_group):
                if not all(k in pixel for k in ['x', 'y', 'color']):
                    return f"Pixel group item {idx} missing required fields"
                if not isinstance(pixel['color'], list) or len(pixel['color']) != 3:
                    return f"Pixel group item {idx} has invalid color"
        
        return None
    
    def to_dict(self, include_runtime: bool = False) -> Dict[str, Any]:
        """
        Convert monitor to dictionary
        
        Args:
            include_runtime: If True, include runtime fields (cooldown state, etc.)
        
        Returns:
            Dictionary representation
        """
        base = {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'target_color': self.target_color,
            'tolerance': self.tolerance,
            'cooldown': self.cooldown,
            'action': self.action,
            'enabled': self.enabled,
            'monitor_type': self.monitor_type,
            'master_id': self.master_id,
            'trigger_mode': self.trigger_mode,
            'pixel_group': self.pixel_group,
            'group_logic': self.group_logic
        }
        
        if include_runtime:
            base.update({
                'in_cooldown': self.in_cooldown,
                'blocked_by_master': self.blocked_by_master,
                'match_count': self.match_count,
                'is_active': self._last_active_state or False
            })
        
        return base
    
    def to_internal_dict(self) -> Dict[str, Any]:
        """Convert to internal dictionary format (includes all fields for processing)"""
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'target_color': self.target_color,
            'tolerance': self.tolerance,
            'cooldown': self.cooldown,
            'action': self.action,
            'enabled': self.enabled,
            'monitor_type': self.monitor_type,
            'master_id': self.master_id,
            'trigger_mode': self.trigger_mode,
            'pixel_group': self.pixel_group,
            'group_logic': self.group_logic,
            'last_trigger_time': self.last_trigger_time,
            'in_cooldown': self.in_cooldown,
            'blocked_by_master': self.blocked_by_master,
            'match_count': self.match_count,
            'last_match': self.last_match,
            '_last_active_state': self._last_active_state
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Monitor':
        """Create Monitor instance from dictionary"""
        return cls(data)
    
    def __repr__(self) -> str:
        return f"Monitor(id={self.id}, name='{self.name}', type={self.monitor_type}, enabled={self.enabled})"

