"""
Image Matching Module
Handles template matching for icon/image detection
"""

import cv2
import numpy as np
from .screen_capture import ScreenCapture
import logging
import os

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ImageMatcher:
    """Template matching for finding images on screen"""
    
    def __init__(self):
        try:
            self.screen_capture = ScreenCapture()
            logger.info("ImageMatcher initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ImageMatcher: {e}")
            raise
    
    def find_template(self, template_path, threshold=0.8, region=None):
        """
        Find a template image on the screen
        
        Args:
            template_path: Path to template image
            threshold: Matching threshold (0-1)
            region: Optional region to search in
        
        Returns:
            Dict with match locations and confidence
        """
        try:
            logger.info(f"Finding template: {template_path}, threshold={threshold}")
            
            # Check if file exists
            if not os.path.exists(template_path):
                logger.error(f"Template file not found: {template_path}")
                return {
                    'success': False,
                    'error': f'Template file not found: {template_path}'
                }
            
            # Load template
            template = cv2.imread(template_path)
            if template is None:
                logger.error(f"Could not load template image: {template_path}")
                return {
                    'success': False,
                    'error': f'Could not load template: {template_path}'
                }
            
            logger.debug(f"Template loaded: shape={template.shape}")
            
            # Capture screen
            screen = self.screen_capture.capture_to_array(region)
            if screen is None:
                logger.error("Failed to capture screen for template matching")
                return {
                    'success': False,
                    'error': 'Failed to capture screen'
                }
            
            logger.debug(f"Screen captured: shape={screen.shape}")
            
            # Convert to grayscale for matching
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # Perform template matching
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            
            # Find locations above threshold
            locations = np.where(result >= threshold)
            matches = []
            
            template_h, template_w = template_gray.shape
            
            for pt in zip(*locations[::-1]):  # Switch x and y
                matches.append({
                    'x': int(pt[0]),
                    'y': int(pt[1]),
                    'width': int(template_w),
                    'height': int(template_h),
                    'center_x': int(pt[0] + template_w / 2),
                    'center_y': int(pt[1] + template_h / 2),
                    'confidence': float(result[pt[1], pt[0]])
                })
            
            # Sort by confidence
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            logger.info(f"Template matching complete: found {len(matches)} match(es)")
            
            return {
                'success': True,
                'found': len(matches) > 0,
                'count': len(matches),
                'matches': matches[:10],  # Limit to top 10 matches
                'threshold': threshold
            }
        
        except Exception as e:
            logger.error(f"Error in template matching: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def find_best_match(self, template_path, threshold=0.8, region=None):
        """
        Find the best matching location for a template
        
        Args:
            template_path: Path to template image
            threshold: Matching threshold (0-1)
            region: Optional region to search in
        
        Returns:
            Dict with best match location or None
        """
        result = self.find_template(template_path, threshold, region)
        
        if result['success'] and result['found']:
            return {
                'success': True,
                'match': result['matches'][0]
            }
        else:
            return {
                'success': False,
                'match': None
            }
    
    def wait_for_image(self, template_path, timeout=5000, check_interval=500, threshold=0.8):
        """
        Wait for an image to appear on screen
        
        Args:
            template_path: Path to template image
            timeout: Maximum wait time in milliseconds
            check_interval: Check interval in milliseconds
            threshold: Matching threshold (0-1)
        
        Returns:
            Dict with match information or None
        """
        import time
        
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < timeout:
            result = self.find_best_match(template_path, threshold)
            
            if result['success'] and result['match']:
                return result['match']
            
            time.sleep(check_interval / 1000)
        
        return None
    
    def image_exists(self, template_path, threshold=0.8, region=None):
        """
        Check if an image exists on screen
        
        Args:
            template_path: Path to template image
            threshold: Matching threshold (0-1)
            region: Optional region to search in
        
        Returns:
            Bool indicating if image exists
        """
        result = self.find_template(template_path, threshold, region)
        return result.get('success', False) and result.get('found', False)

