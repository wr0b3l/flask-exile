"""
Pixel Monitor - Continuous pixel monitoring with actions
Monitors specified pixels and triggers keyboard actions on color changes
"""

import time
import pydirectinput
from PIL import ImageGrab
from datetime import datetime


class PixelMonitor:
    def __init__(self):
        self.monitors = []  # List of pixel monitors
        self.running = False
        self.check_interval = 0.1  # 100ms = 10 checks per second
        
    def add_monitor(self, x, y, target_color, action, tolerance=10, name=""):
        """
        Add a pixel to monitor
        
        Args:
            x, y: Screen coordinates
            target_color: (r, g, b) tuple
            action: Dictionary with action type and parameters
                    {'type': 'keypress', 'key': 'space'}
                    {'type': 'callback', 'function': my_function}
            tolerance: Color difference tolerance
            name: Optional name for this monitor
        """
        monitor = {
            'x': x,
            'y': y,
            'target_color': target_color,
            'action': action,
            'tolerance': tolerance,
            'name': name or f"Monitor_{len(self.monitors)+1}",
            'last_match': None,
            'match_count': 0
        }
        self.monitors.append(monitor)
        print(f"✓ Added monitor: {monitor['name']} at ({x}, {y})")
        return len(self.monitors) - 1
    
    def remove_monitor(self, index):
        """Remove a monitor by index"""
        if 0 <= index < len(self.monitors):
            removed = self.monitors.pop(index)
            print(f"✓ Removed monitor: {removed['name']}")
            return True
        return False
    
    def check_pixel(self, monitor):
        """Check if a pixel matches target color"""
        try:
            x, y = monitor['x'], monitor['y']
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            current = screenshot.getpixel((0, 0))[:3]
            
            # Calculate color difference
            diff = sum(abs(current[i] - monitor['target_color'][i]) for i in range(3))
            
            return diff <= monitor['tolerance'], current
            
        except Exception as e:
            print(f"✗ Error checking {monitor['name']}: {e}")
            return False, None
    
    def execute_action(self, monitor, current_color):
        """Execute the action for a matched pixel"""
        action = monitor['action']
        
        try:
            if action['type'] == 'keypress':
                key = action['key']
                print(f"[{monitor['name']}] Pressing key: {key}")
                pydirectinput.press(key)
                
            elif action['type'] == 'hotkey':
                keys = action['keys']  # List of keys like ['ctrl', 'c']
                print(f"[{monitor['name']}] Pressing hotkey: {'+'.join(keys)}")
                # pydirectinput doesn't have hotkey, so we need to press keys sequentially
                for key in keys[:-1]:
                    pydirectinput.keyDown(key)
                pydirectinput.press(keys[-1])
                for key in reversed(keys[:-1]):
                    pydirectinput.keyUp(key)
                
            elif action['type'] == 'click':
                x, y = action.get('x', monitor['x']), action.get('y', monitor['y'])
                button = action.get('button', 'left')
                print(f"[{monitor['name']}] Clicking at ({x}, {y})")
                pydirectinput.click(x, y, button=button)
                
            elif action['type'] == 'callback':
                func = action['function']
                print(f"[{monitor['name']}] Calling callback")
                func(monitor, current_color)
                
            elif action['type'] == 'log':
                print(f"[{monitor['name']}] Color matched: RGB{current_color}")
            
            monitor['last_match'] = datetime.now()
            monitor['match_count'] += 1
            
        except Exception as e:
            print(f"✗ Error executing action for {monitor['name']}: {e}")
    
    def run(self):
        """Start monitoring all pixels"""
        self.running = True
        print(f"\n{'='*60}")
        print(f"Pixel Monitor Started")
        print(f"{'='*60}")
        print(f"Monitoring {len(self.monitors)} pixel(s)")
        print(f"Check interval: {self.check_interval}s ({1/self.check_interval:.0f} checks/sec)")
        print(f"Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        try:
            while self.running:
                for monitor in self.monitors:
                    is_match, current_color = self.check_pixel(monitor)
                    
                    if is_match:
                        self.execute_action(monitor, current_color)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print(f"\n\n{'='*60}")
            print("Monitoring stopped by user")
            self.print_stats()
            print(f"{'='*60}")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
    
    def print_stats(self):
        """Print monitoring statistics"""
        print("\nMonitoring Statistics:")
        for i, monitor in enumerate(self.monitors):
            print(f"\n{i+1}. {monitor['name']}")
            print(f"   Position: ({monitor['x']}, {monitor['y']})")
            print(f"   Target: RGB{monitor['target_color']}")
            print(f"   Matches: {monitor['match_count']}")
            if monitor['last_match']:
                print(f"   Last match: {monitor['last_match'].strftime('%H:%M:%S')}")
    
