"""
Monitoring Loop Service - Background thread for continuous pixel monitoring
"""
import logging
import time
import threading
from typing import Dict, Any, Tuple, Callable
from config import Config
from pixel_monitor import PixelMonitor

logger = logging.getLogger(__name__)


class MonitoringLoop:
    """Service for running the background monitoring loop"""
    
    def __init__(self, monitor_service, socketio):
        """
        Initialize monitoring loop
        
        Args:
            monitor_service: MonitorService instance
            socketio: SocketIO instance for emitting events
        """
        self.monitor_service = monitor_service
        self.socketio = socketio
        self.pixel_monitor = PixelMonitor()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the monitoring thread"""
        if not self.running and self.monitor_service.count() > 0:
            self.running = True
            self.pixel_monitor.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            logger.info("Pixel monitoring started")
    
    def stop(self):
        """Stop the monitoring thread"""
        if self.running:
            self.running = False
            self.pixel_monitor.running = False
            logger.info("Pixel monitoring stopped")
    
    def is_running(self) -> bool:
        """Check if monitoring is currently running"""
        return self.running
    
    def check_monitor_pixels(self, monitor: Dict[str, Any]) -> Tuple[bool, bool, Dict[str, Tuple[int, int, int]]]:
        """
        Check all pixels for a monitor (main pixel + pixel_group)
        
        Args:
            monitor: Monitor dictionary
        
        Returns:
            Tuple of (all_matched, any_matched, colors_dict)
        """
        # Check main pixel
        main_matched, main_color = self.pixel_monitor.check_pixel(monitor)
        colors = {'main': main_color}
        
        pixel_group = monitor.get('pixel_group', [])
        if not pixel_group:
            # No additional pixels, return main result
            return main_matched, main_matched, colors
        
        # Check additional pixels
        group_matches = [main_matched]
        for idx, pixel in enumerate(pixel_group):
            # Create temporary monitor object for pixel check
            temp_monitor = {
                'x': pixel['x'],
                'y': pixel['y'],
                'target_color': pixel['color'],
                'tolerance': pixel.get('tolerance', monitor.get('tolerance', Config.DEFAULT_TOLERANCE))
            }
            matched, color = self.pixel_monitor.check_pixel(temp_monitor)
            group_matches.append(matched)
            colors[f'pixel_{idx+1}'] = color
        
        all_matched = all(group_matches)
        any_matched = any(group_matches)
        
        return all_matched, any_matched, colors
    
    def _run_loop(self):
        """Background thread that continuously checks all monitors"""
        while self.running:
            try:
                current_time = time.time() * 1000  # Current time in milliseconds
                monitors = self.monitor_service.get_all()
                
                # PHASE 1: Check all MASTER monitors first
                master_states = {}  # Store master states: {master_id: is_active}
                
                for monitor in monitors:
                    if monitor.get('monitor_type') != 'master':
                        continue
                    
                    if not monitor.get('enabled', True):
                        master_states[monitor['id']] = False
                        continue
                    
                    # Check master pixels (main + pixel_group)
                    all_matched, any_matched, colors = self.check_monitor_pixels(monitor)
                    trigger_mode = monitor.get('trigger_mode', 'no_match')
                    group_logic = monitor.get('group_logic', 'all_match')
                    
                    # Determine if pixels match based on group logic
                    pixels_match = all_matched if group_logic == 'all_match' else any_matched
                    
                    # Master is "active" based on trigger mode and pixel results
                    # 'match' = active when pixels match (UI visible)
                    # 'no_match' = active when pixels don't match
                    is_active = pixels_match if trigger_mode == 'match' else not pixels_match
                    master_states[monitor['id']] = is_active
                    
                    # Log master state changes
                    previous_state = monitor.get('_last_active_state', None)
                    if previous_state != is_active:
                        monitor['_last_active_state'] = is_active
                        state_text = 'ACTIVE' if is_active else 'INACTIVE'
                        logger.info(f"Master '{monitor['name']}' state changed: {state_text}")
                        
                        # Emit activity log
                        self.socketio.emit('activity_log', {
                            'type': 'info' if is_active else 'warning',
                            'message': f"Master '{monitor['name']}' {state_text.lower()}"
                        })
                        
                        # Emit master state change for UI updates
                        self.socketio.emit('master_state_change', {
                            'id': monitor['id'],
                            'is_active': is_active
                        })
                
                # PHASE 2: Check SLAVE and NORMAL monitors
                for monitor in monitors:
                    monitor_type = monitor.get('monitor_type', 'normal')
                    
                    if monitor_type == 'master':
                        continue  # Already processed
                    
                    if not monitor.get('enabled', True):
                        # Monitor is paused/disabled - clear states
                        self._clear_monitor_states(monitor)
                        continue
                    
                    # Check if slave is blocked by master
                    if monitor_type == 'slave':
                        master_id = monitor.get('master_id')
                        master_is_active = master_states.get(master_id, False)
                        
                        if not master_is_active:
                            # Slave is blocked
                            if not monitor.get('blocked_by_master', False):
                                monitor['blocked_by_master'] = True
                                logger.info(f"Slave '{monitor['name']}' blocked by master (ID: {master_id})")
                                self.socketio.emit('monitor_state_change', {
                                    'id': monitor['id'],
                                    'blocked_by_master': True
                                })
                            continue  # Skip this slave
                        else:
                            # Slave is unblocked
                            if monitor.get('blocked_by_master', False):
                                monitor['blocked_by_master'] = False
                                logger.info(f"Slave '{monitor['name']}' unblocked by master (ID: {master_id})")
                                self.socketio.emit('monitor_state_change', {
                                    'id': monitor['id'],
                                    'blocked_by_master': False
                                })
                    
                    # Check cooldown status
                    cooldown = monitor.get('cooldown', Config.DEFAULT_COOLDOWN)
                    last_trigger = monitor.get('last_trigger_time', 0)
                    time_since_last_trigger = current_time - last_trigger
                    in_cooldown = time_since_last_trigger < cooldown
                    
                    # If still in cooldown, skip checking and triggering
                    if in_cooldown:
                        continue
                    
                    # Cooldown has expired - check pixels (main + pixel_group)
                    all_matched, any_matched, colors = self.check_monitor_pixels(monitor)
                    trigger_mode = monitor.get('trigger_mode', 'no_match')
                    group_logic = monitor.get('group_logic', 'all_match')
                    
                    # Determine if pixels match based on group logic
                    pixels_match = all_matched if group_logic == 'all_match' else any_matched
                    
                    # Determine if action should trigger based on mode
                    should_trigger = (not pixels_match) if trigger_mode == 'no_match' else pixels_match
                    
                    # Get main color for logging (backward compatibility)
                    current_color = colors.get('main')
                    
                    # Action triggers based on trigger mode
                    if should_trigger:
                        self._trigger_action(monitor, current_color, monitor_type, current_time)
                    else:
                        # Pixel matches, cooldown expired, clear cooldown state if set
                        if monitor.get('in_cooldown', False):
                            monitor['in_cooldown'] = False
                            self.socketio.emit('monitor_state_change', {
                                'id': monitor['id'],
                                'in_cooldown': False
                            })
                
                time.sleep(Config.MONITOR_CHECK_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}", exc_info=True)
                time.sleep(1)
    
    def _clear_monitor_states(self, monitor: Dict[str, Any]):
        """Clear cooldown and blocked states when monitor is disabled"""
        if monitor.get('in_cooldown', False):
            monitor['in_cooldown'] = False
            self.socketio.emit('monitor_state_change', {
                'id': monitor['id'],
                'in_cooldown': False
            })
        if monitor.get('blocked_by_master', False):
            monitor['blocked_by_master'] = False
            self.socketio.emit('monitor_state_change', {
                'id': monitor['id'],
                'blocked_by_master': False
            })
    
    def _trigger_action(self, monitor: Dict[str, Any], current_color: Tuple[int, int, int], 
                       monitor_type: str, current_time: float):
        """Execute action when monitor triggers"""
        logger.info(
            f"Monitor '{monitor['name']}' (ID: {monitor['id']}, type: {monitor_type}, "
            f"enabled: {monitor.get('enabled', True)}) detected change at "
            f"({monitor['x']}, {monitor['y']}) - Current: RGB{current_color}, "
            f"Target: RGB{monitor['target_color']}"
        )
        
        # Update last trigger time and set cooldown state
        monitor['last_trigger_time'] = current_time
        monitor['match_count'] = monitor.get('match_count', 0) + 1
        monitor['in_cooldown'] = True
        
        # Execute action
        self.pixel_monitor.execute_action(monitor, current_color)
        
        # Emit events to dashboard
        self.socketio.emit('monitor_match', {
            'id': monitor['id'],
            'name': monitor['name'],
            'x': monitor['x'],
            'y': monitor['y'],
            'current_color': current_color,
            'target_color': monitor['target_color']
        })
        
        self.socketio.emit('action_triggered', {
            'monitor': monitor['name'],
            'action': monitor['action']
        })
        
        self.socketio.emit('monitor_state_change', {
            'id': monitor['id'],
            'in_cooldown': True
        })

