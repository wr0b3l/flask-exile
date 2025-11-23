"""
Screen Capture Module
Handles screen capturing using mss library
"""

import mss
import mss.tools
from PIL import Image
import numpy as np
import io
import base64
from datetime import datetime
import logging

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ScreenCapture:
    """Screen capture functionality using mss"""
    
    def __init__(self):
        try:
            self.sct = mss.mss()
            logger.info("ScreenCapture initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ScreenCapture: {e}")
            raise
    
    def capture(self, region=None, save_path=None):
        """
        Capture screen or a specific region
        
        Args:
            region: Dict with {x, y, width, height} or None for full screen
            save_path: Optional path to save the screenshot
        
        Returns:
            Dict with success status and image data
        """
        try:
            logger.info(f"Capturing screen - region: {region}, save_path: {save_path}")
            
            # Determine capture region
            if region:
                monitor = {
                    "top": region['y'],
                    "left": region['x'],
                    "width": region['width'],
                    "height": region['height']
                }
                logger.debug(f"Using custom region: {monitor}")
            else:
                # Capture primary monitor
                monitor = self.sct.monitors[1]
                logger.debug(f"Using primary monitor: {monitor}")
            
            # Capture screenshot
            sct_img = self.sct.grab(monitor)
            logger.debug(f"Screenshot captured: {sct_img.size}")
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            
            # Save if path provided
            if save_path:
                img.save(save_path)
                logger.info(f"Screenshot saved to: {save_path}")
            
            # Convert to base64 for API response
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            logger.info(f"Screen capture successful: {sct_img.size[0]}x{sct_img.size[1]}")
            
            return {
                'success': True,
                'width': sct_img.size[0],
                'height': sct_img.size[1],
                'timestamp': datetime.now().isoformat(),
                'image_base64': img_base64
            }
        
        except Exception as e:
            logger.error(f"Screen capture failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def capture_to_array(self, region=None):
        """
        Capture screen and return as numpy array
        
        Args:
            region: Dict with {x, y, width, height} or None for full screen
        
        Returns:
            numpy array of the image (BGR format for OpenCV)
        """
        try:
            logger.debug(f"Capturing to array - region: {region}")
            
            if region:
                monitor = {
                    "top": region['y'],
                    "left": region['x'],
                    "width": region['width'],
                    "height": region['height']
                }
            else:
                monitor = self.sct.monitors[1]
            
            sct_img = self.sct.grab(monitor)
            # Convert to numpy array (RGB)
            img = np.array(sct_img)
            # Convert RGB to BGR for OpenCV
            img_bgr = img[:, :, [2, 1, 0]]
            
            logger.debug(f"Array capture successful: shape={img_bgr.shape}")
            return img_bgr
        
        except Exception as e:
            logger.error(f"Error capturing screen to array: {e}", exc_info=True)
            return None
    
    def get_monitors(self):
        """Get information about all monitors"""
        try:
            monitors = []
            for i, monitor in enumerate(self.sct.monitors[1:], 1):  # Skip the "all monitors" entry
                monitors.append({
                    'id': i,
                    'x': monitor['left'],
                    'y': monitor['top'],
                    'width': monitor['width'],
                    'height': monitor['height']
                })
            logger.info(f"Found {len(monitors)} monitor(s)")
            return monitors
        except Exception as e:
            logger.error(f"Error getting monitors: {e}", exc_info=True)
            return []

