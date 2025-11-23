"""
Text Reader Module
Handles OCR text recognition using pytesseract
"""

import pytesseract
from PIL import Image
import numpy as np
from .screen_capture import ScreenCapture
import logging

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class TextReader:
    """OCR text recognition from screen"""
    
    def __init__(self):
        try:
            self.screen_capture = ScreenCapture()
            # Set tesseract path for this system
            pytesseract.pytesseract.tesseract_cmd = r'G:\tesseract\tesseract.exe'
            logger.info("TextReader initialized successfully with Tesseract at G:\\tesseract")
        except Exception as e:
            logger.error(f"Failed to initialize TextReader: {e}")
            raise
    
    def read_text(self, region=None, lang='eng', config=''):
        """
        Read text from screen using OCR
        
        Args:
            region: Optional region to read from
            lang: Language for OCR (default: 'eng')
            config: Additional tesseract configuration
        
        Returns:
            Dict with recognized text
        """
        try:
            logger.info(f"Reading text from screen - lang={lang}, region={region}")
            
            # Capture screen
            img = self.screen_capture.capture_to_array(region)
            
            if img is None:
                logger.error("Failed to capture screen for OCR")
                return {
                    'success': False,
                    'error': 'Failed to capture screen'
                }
            
            # Convert BGR to RGB for PIL
            img_rgb = img[:, :, [2, 1, 0]]
            pil_img = Image.fromarray(img_rgb)
            
            logger.debug(f"Image prepared for OCR: size={pil_img.size}")
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_img, lang=lang, config=config)
            
            logger.debug(f"OCR text extraction complete: {len(text)} characters")
            
            # Get detailed data with bounding boxes
            data = pytesseract.image_to_data(pil_img, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Extract words with positions
            words = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Filter out low confidence
                    words.append({
                        'text': data['text'][i],
                        'confidence': int(data['conf'][i]),
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
            
            word_count = len([w for w in words if w['text'].strip()])
            logger.info(f"OCR complete: {word_count} words found")
            
            return {
                'success': True,
                'text': text.strip(),
                'words': words,
                'word_count': word_count
            }
        
        except pytesseract.TesseractNotFoundError as e:
            logger.error("Tesseract not found - please install Tesseract OCR")
            return {
                'success': False,
                'error': 'tesseract is not installed or it\'s not in your PATH. See README file for more information.',
                'error_type': 'TesseractNotFoundError'
            }
        except Exception as e:
            logger.error(f"Error reading text: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def find_text(self, search_text, region=None, case_sensitive=False):
        """
        Search for specific text on screen
        
        Args:
            search_text: Text to search for
            region: Optional region to search in
            case_sensitive: Whether search is case sensitive
        
        Returns:
            Dict with found text locations
        """
        try:
            result = self.read_text(region)
            
            if not result['success']:
                return result
            
            # Search in recognized text
            full_text = result['text']
            if not case_sensitive:
                full_text = full_text.lower()
                search_text = search_text.lower()
            
            found = search_text in full_text
            
            # Find matching words
            matches = []
            for word in result['words']:
                word_text = word['text'] if case_sensitive else word['text'].lower()
                if search_text in word_text:
                    matches.append(word)
            
            return {
                'success': True,
                'found': found,
                'matches': matches,
                'search_text': search_text
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def wait_for_text(self, search_text, timeout=5000, check_interval=500, region=None):
        """
        Wait for text to appear on screen
        
        Args:
            search_text: Text to wait for
            timeout: Maximum wait time in milliseconds
            check_interval: Check interval in milliseconds
            region: Optional region to search in
        
        Returns:
            Bool indicating if text was found
        """
        import time
        
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < timeout:
            result = self.find_text(search_text, region)
            
            if result.get('success') and result.get('found'):
                return True
            
            time.sleep(check_interval / 1000)
        
        return False

