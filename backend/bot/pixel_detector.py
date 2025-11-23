"""
Pixel Detection Module
Handles pixel color detection and matching
"""

import numpy as np
from .screen_capture import ScreenCapture
import logging

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class PixelDetector:
    """Pixel color detection and matching"""
    
    def __init__(self):
        try:
            self.screen_capture = ScreenCapture()
            logger.info("PixelDetector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PixelDetector: {e}")
            raise
    
    def get_pixel_color(self, x, y):
        """
        Get the RGB color at specific coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
        
        Returns:
            Dict with color information
        """
        try:
            logger.info(f"Getting pixel color at ({x}, {y})")
            
            # Capture 1x1 region at the specified coordinates
            region = {'x': x, 'y': y, 'width': 1, 'height': 1}
            img = self.screen_capture.capture_to_array(region)
            
            if img is None:
                logger.error(f"Failed to capture screen at ({x}, {y})")
                return {'success': False, 'error': 'Failed to capture screen'}
            
            # Get color (BGR to RGB)
            b, g, r = img[0, 0]
            
            result = {
                'success': True,
                'x': x,
                'y': y,
                'color': {
                    'r': int(r),
                    'g': int(g),
                    'b': int(b),
                    'hex': f'#{r:02x}{g:02x}{b:02x}'
                }
            }
            
            logger.info(f"Pixel color at ({x}, {y}): RGB({r}, {g}, {b}) = {result['color']['hex']}")
            return result
        
        except Exception as e:
            logger.error(f"Error getting pixel color at ({x}, {y}): {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def find_color(self, target_color, tolerance=0, region=None):
        """
        Find all pixels matching a specific color
        
        Args:
            target_color: RGB color to find [r, g, b]
            tolerance: Color tolerance (0-255)
            region: Optional region to search in
        
        Returns:
            Dict with matching pixel locations
        """
        try:
            logger.info(f"Finding color RGB{target_color} with tolerance={tolerance}")
            
            img = self.screen_capture.capture_to_array(region)
            
            if img is None:
                logger.error("Failed to capture screen for color finding")
                return {'success': False, 'error': 'Failed to capture screen'}
            
            # Convert BGR to RGB
            img_rgb = img[:, :, [2, 1, 0]]
            
            # Create color range
            target = np.array(target_color)
            lower = np.clip(target - tolerance, 0, 255)
            upper = np.clip(target + tolerance, 0, 255)
            
            # Find matching pixels
            mask = np.all((img_rgb >= lower) & (img_rgb <= upper), axis=2)
            locations = np.argwhere(mask)
            
            # Convert to list of coordinates
            matches = [{'x': int(loc[1]), 'y': int(loc[0])} for loc in locations[:100]]  # Limit to 100
            
            logger.info(f"Found {len(locations)} matching pixels (showing first 100)")
            
            return {
                'success': True,
                'count': len(locations),
                'matches': matches,
                'target_color': target_color,
                'tolerance': tolerance
            }
        
        except Exception as e:
            logger.error(f"Error finding color: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def wait_for_color(self, target_color, x, y, timeout=5000, check_interval=100):
        """
        Wait for a specific color to appear at coordinates
        
        Args:
            target_color: RGB color to wait for
            x, y: Coordinates to check
            timeout: Maximum wait time in milliseconds
            check_interval: Check interval in milliseconds
        
        Returns:
            Bool indicating if color was found
        """
        import time
        
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < timeout:
            result = self.get_pixel_color(x, y)
            
            if result['success']:
                color = [
                    result['color']['r'],
                    result['color']['g'],
                    result['color']['b']
                ]
                if color == target_color:
                    return True
            
            time.sleep(check_interval / 1000)
        
        return False
    
    def color_exists(self, target_color, tolerance=0, region=None):
        """
        Check if a color exists on screen
        
        Args:
            target_color: RGB color to find
            tolerance: Color tolerance
            region: Optional region to search
        
        Returns:
            Bool indicating if color exists
        """
        result = self.find_color(target_color, tolerance, region)
        return result.get('success', False) and result.get('count', 0) > 0

