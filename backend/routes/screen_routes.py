"""
Screen Routes - Screen capture operations
"""
from flask import Blueprint, jsonify, request
import logging
from bot.screen_capture import ScreenCapture

logger = logging.getLogger(__name__)

screen_bp = Blueprint('screen', __name__, url_prefix='/api/screen')


def get_screen_capture():
    """Create a fresh ScreenCapture instance for thread safety"""
    return ScreenCapture()


@screen_bp.route('/capture', methods=['POST'])
def capture_screen():
    """Capture a screenshot"""
    try:
        data = request.get_json() or {}
        region = data.get('region', None)  # Optional region: {x, y, width, height}
        
        sc = get_screen_capture()
        result = sc.capture(region)
        
        if result['success']:
            logger.info(f"Screen capture successful via API")
            return jsonify(result)
        else:
            logger.error(f"Screen capture failed: {result.get('error')}")
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Exception in capture_screen endpoint: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e), 'error_type': type(e).__name__}), 500

