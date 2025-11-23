"""
Pixel Routes - Pixel detection and color operations
"""
from flask import Blueprint, jsonify, request
import logging
from bot.pixel_detector import PixelDetector

logger = logging.getLogger(__name__)

pixel_bp = Blueprint('pixel', __name__, url_prefix='/api/pixel')


def get_pixel_detector():
    """Create a fresh PixelDetector instance for thread safety"""
    return PixelDetector()


@pixel_bp.route('/get-color', methods=['POST'])
def get_pixel_color():
    """Get color at specific coordinates"""
    try:
        data = request.get_json() or {}
        x = data.get('x')
        y = data.get('y')
        
        if x is None or y is None:
            logger.warning("Missing x or y coordinates in request")
            return jsonify({'success': False, 'error': 'Missing x or y coordinates'}), 400
        
        pd = get_pixel_detector()
        result = pd.get_pixel_color(x, y)
        
        if result['success']:
            logger.info(f"Got pixel color at ({x}, {y}): {result['color']['hex']}")
        else:
            logger.error(f"Failed to get pixel color: {result.get('error')}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Exception in get_pixel_color endpoint: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e), 'error_type': type(e).__name__}), 500


@pixel_bp.route('/find-color', methods=['POST'])
def find_color():
    """Find all pixels matching a specific color"""
    try:
        data = request.get_json() or {}
        color = data.get('color')  # RGB tuple [r, g, b]
        tolerance = data.get('tolerance', 0)
        region = data.get('region', None)
        
        if not color:
            logger.warning("Missing color parameter in request")
            return jsonify({'success': False, 'error': 'Missing color parameter'}), 400
        
        pd = get_pixel_detector()
        result = pd.find_color(color, tolerance, region)
        
        if result['success']:
            logger.info(f"Found {result['count']} pixels matching {color}")
        else:
            logger.error(f"Failed to find color: {result.get('error')}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Exception in find_color endpoint: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e), 'error_type': type(e).__name__}), 500


def init_pixel_routes(socketio):
    """
    Initialize pixel routes with dependencies
    
    Args:
        socketio: SocketIO instance
    """
    
    @pixel_bp.route('/detected', methods=['POST'])
    def pixel_detected():
        """Receive pixel data from desktop picker"""
        try:
            data = request.get_json() or {}
            
            logger.info(f"Pixel detected: ({data.get('x')}, {data.get('y')}) = {data.get('hex')}")
            
            # Broadcast to all connected clients via WebSocket
            socketio.emit('pixel_picked', data)
            
            return jsonify({
                'success': True,
                'message': 'Pixel data received',
                'pixel': data
            })
        except Exception as e:
            logger.error(f"Exception in pixel_detected endpoint: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return pixel_bp

