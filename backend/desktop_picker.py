"""
Desktop Pixel Picker - System-wide pixel selection
Uses PyAutoGUI for cross-platform mouse/keyboard control
Creates a transparent fullscreen overlay for pixel picking
"""

import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import ImageGrab
import requests
import sys

class PixelPickerOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Semi-transparent
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg='blue')
        
        # Labels
        self.info_label = tk.Label(
            self.root,
            text="Move mouse to position, then click to select pixel\nPress ESC to cancel",
            font=('Arial', 16, 'bold'),
            bg='black',
            fg='white',
            padx=20,
            pady=10
        )
        self.info_label.pack(pady=20)
        
        self.coord_label = tk.Label(
            self.root,
            text="Position: (0, 0)",
            font=('Arial', 14),
            bg='black',
            fg='yellow',
            padx=20,
            pady=5
        )
        self.coord_label.pack()
        
        # Crosshair
        self.canvas = tk.Canvas(self.root, bg='blue', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Bind events
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('<Escape>', self.on_cancel)
        
        self.selected_pixel = None
        
    def on_mouse_move(self, event):
        """Update crosshair position and coordinates"""
        # Get absolute screen coordinates
        x = event.x_root
        y = event.y_root
        self.coord_label.config(text=f"Position: ({x}, {y})")
        
        # Draw crosshair
        self.canvas.delete('crosshair')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Vertical line
        self.canvas.create_line(event.x, 0, event.x, screen_height, fill='red', width=2, tags='crosshair')
        # Horizontal line
        self.canvas.create_line(0, event.y, screen_width, event.y, fill='red', width=2, tags='crosshair')
        # Center dot
        self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='red', outline='white', width=2, tags='crosshair')
        
    def on_click(self, event):
        """Capture pixel at click position"""
        # Get absolute screen coordinates
        x = event.x_root
        y = event.y_root
        
        # Hide overlay temporarily to capture correct color
        self.root.withdraw()
        self.root.update()
        
        # Get pixel color
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel = screenshot.getpixel((0, 0))
            r, g, b = pixel[:3]  # Handle both RGB and RGBA
            
            self.selected_pixel = {
                'x': x,
                'y': y,
                'r': r,
                'g': g,
                'b': b,
                'hex': f'#{r:02x}{g:02x}{b:02x}'
            }
            
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture pixel: {e}")
            self.root.deiconify()
    
    def on_cancel(self, event):
        """Cancel pixel selection"""
        self.selected_pixel = None
        self.root.quit()
    
    def run(self):
        """Show picker and wait for selection"""
        self.root.mainloop()
        self.root.destroy()
        return self.selected_pixel


def pick_pixel():
    """Launch pixel picker and return selected pixel data"""
    print("Starting pixel picker...")
    print("Move mouse to desired location and click")
    print("Press ESC to cancel")
    
    picker = PixelPickerOverlay()
    result = picker.run()
    
    if result:
        print(f"\n[OK] Pixel selected:")
        print(f"  Position: ({result['x']}, {result['y']})")
        print(f"  Color: RGB({result['r']}, {result['g']}, {result['b']}) = {result['hex']}")
        return result
    else:
        print("\n[CANCEL] Selection cancelled")
        return None


def monitor_pixel(x, y, target_color, callback, tolerance=10):
    """
    Monitor a pixel for color changes
    
    Args:
        x, y: Pixel coordinates
        target_color: (r, g, b) tuple to watch for
        callback: Function to call when color changes
        tolerance: Color difference tolerance (0-255)
    """
    import time
    
    print(f"\nMonitoring pixel at ({x}, {y})")
    print(f"Target color: RGB{target_color}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Capture pixel
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            current = screenshot.getpixel((0, 0))[:3]
            
            # Check if color matches (within tolerance)
            diff = sum(abs(current[i] - target_color[i]) for i in range(3))
            
            if diff <= tolerance:
                print(f"[MATCH] Color match detected at ({x}, {y}): RGB{current}")
                callback()
            
            time.sleep(0.1)  # Check 10 times per second
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")


def press_key(key):
    """Simulate keyboard press"""
    print(f"Pressing key: {key}")
    pyautogui.press(key)


# Example usage
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Desktop Pixel Picker')
    parser.add_argument('--pick', action='store_true', help='Pick a pixel')
    parser.add_argument('--monitor', nargs=2, type=int, metavar=('X', 'Y'), help='Monitor pixel at X Y')
    parser.add_argument('--color', nargs=3, type=int, metavar=('R', 'G', 'B'), help='Target RGB color')
    parser.add_argument('--key', default='space', help='Key to press on match')
    parser.add_argument('--tolerance', type=int, default=10, help='Color tolerance (0-255)')
    
    args = parser.parse_args()
    
    if args.pick:
        # Pick a pixel
        result = pick_pixel()
        if result:
            # Send to backend
            try:
                response = requests.post(
                    'http://localhost:5000/api/pixel/detected',
                    json=result
                )
                print(f"\n[OK] Sent to backend: {response.status_code}")
            except Exception as e:
                print(f"\n[ERROR] Failed to send to backend: {e}")
    
    elif args.monitor and args.color:
        # Monitor a pixel
        x, y = args.monitor
        target = tuple(args.color)
        
        def on_match():
            press_key(args.key)
        
        monitor_pixel(x, y, target, on_match, args.tolerance)
    
    else:
        parser.print_help()

