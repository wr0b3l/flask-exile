"""
Monitor Service - CRUD operations for monitors
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from models import Monitor

logger = logging.getLogger(__name__)


class MonitorService:
    """Service for managing monitor lifecycle"""
    
    def __init__(self):
        """Initialize monitor service"""
        self.monitors: List[Dict[str, Any]] = []
        self._next_id = 1
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all monitors"""
        return self.monitors
    
    def get_by_id(self, monitor_id: int) -> Optional[Dict[str, Any]]:
        """
        Get monitor by ID
        
        Args:
            monitor_id: Monitor ID
        
        Returns:
            Monitor dictionary or None if not found
        """
        return next((m for m in self.monitors if m['id'] == monitor_id), None)
    
    def add(self, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Add a new monitor
        
        Args:
            data: Monitor data dictionary
        
        Returns:
            Tuple of (success, message, monitor_dict or None)
        """
        try:
            # Assign ID if not provided
            if 'id' not in data:
                data['id'] = self._next_id
                self._next_id += 1
            
            # Create Monitor instance for validation
            monitor = Monitor(data)
            error = monitor.validate()
            if error:
                return False, error, None
            
            # Convert to internal dict and add to list
            monitor_dict = monitor.to_internal_dict()
            self.monitors.append(monitor_dict)
            
            # Update next ID
            self._next_id = max(self._next_id, data['id'] + 1)
            
            logger.info(f"Added monitor: {monitor_dict['name']} at ({monitor_dict['x']}, {monitor_dict['y']})")
            return True, "Monitor added successfully", monitor_dict
            
        except Exception as e:
            logger.error(f"Error adding monitor: {e}", exc_info=True)
            return False, str(e), None
    
    def update(self, monitor_id: int, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Update an existing monitor
        
        Args:
            monitor_id: Monitor ID
            data: Updated monitor data (partial or full)
        
        Returns:
            Tuple of (success, message, monitor_dict or None)
        """
        monitor = self.get_by_id(monitor_id)
        if not monitor:
            return False, f"Monitor {monitor_id} not found", None
        
        try:
            changed_fields = []
            
            # Update allowed fields and track changes
            updatable_fields = [
                'name', 'x', 'y', 'target_color', 'tolerance', 'cooldown',
                'action', 'monitor_type', 'master_id', 'trigger_mode',
                'pixel_group', 'group_logic'
            ]
            
            for field in updatable_fields:
                if field in data and data[field] != monitor.get(field):
                    old_value = monitor.get(field)
                    monitor[field] = data[field]
                    
                    # Track change for logging
                    if field == 'name':
                        changed_fields.append(f"name: '{old_value}' → '{data[field]}'")
                    elif field in ['x', 'y', 'tolerance', 'cooldown']:
                        changed_fields.append(f"{field}: {old_value} → {data[field]}")
                    else:
                        changed_fields.append(f"{field} changed")
            
            if changed_fields:
                logger.info(f"Updated monitor {monitor_id} ({monitor['name']}): {', '.join(changed_fields)}")
            
            return True, "Monitor updated successfully", monitor
            
        except Exception as e:
            logger.error(f"Error updating monitor: {e}", exc_info=True)
            return False, str(e), None
    
    def toggle(self, monitor_id: int) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Toggle monitor enabled state
        
        Args:
            monitor_id: Monitor ID
        
        Returns:
            Tuple of (success, message, monitor_dict or None)
        """
        monitor = self.get_by_id(monitor_id)
        if not monitor:
            return False, f"Monitor {monitor_id} not found", None
        
        try:
            logger.info(f"Toggle request for monitor {monitor_id} - Current enabled state: {monitor.get('enabled', True)}")
            
            monitor['enabled'] = not monitor['enabled']
            status = 'resumed' if monitor['enabled'] else 'paused'
            
            logger.info(f"Monitor {monitor_id} ({monitor['name']}): {status} - New enabled state: {monitor['enabled']}")
            
            return True, status, monitor
            
        except Exception as e:
            logger.error(f"Error toggling monitor: {e}", exc_info=True)
            return False, str(e), None
    
    def remove(self, monitor_id: int) -> Tuple[bool, str, Optional[str]]:
        """
        Remove a monitor
        
        Args:
            monitor_id: Monitor ID
        
        Returns:
            Tuple of (success, message, monitor_name or None)
        """
        monitor = self.get_by_id(monitor_id)
        if not monitor:
            return False, f"Monitor {monitor_id} not found", None
        
        try:
            monitor_name = monitor['name']
            self.monitors = [m for m in self.monitors if m['id'] != monitor_id]
            logger.info(f"Removed monitor: {monitor_name} (ID: {monitor_id})")
            return True, "Monitor removed successfully", monitor_name
            
        except Exception as e:
            logger.error(f"Error removing monitor: {e}", exc_info=True)
            return False, str(e), None
    
    def load_monitors(self, monitors: List[Dict[str, Any]]):
        """
        Load monitors from external source (e.g., persistence)
        
        Args:
            monitors: List of monitor dictionaries
        """
        self.monitors = monitors
        
        # Update next ID
        if monitors:
            max_id = max(m['id'] for m in monitors)
            self._next_id = max_id + 1
        else:
            self._next_id = 1
        
        logger.info(f"Loaded {len(monitors)} monitors into service")
    
    def count(self) -> int:
        """Get total number of monitors"""
        return len(self.monitors)
    
    def count_by_type(self) -> Dict[str, int]:
        """Get count of monitors by type"""
        counts = {'master': 0, 'slave': 0, 'normal': 0}
        for monitor in self.monitors:
            monitor_type = monitor.get('monitor_type', 'normal')
            counts[monitor_type] = counts.get(monitor_type, 0) + 1
        return counts

