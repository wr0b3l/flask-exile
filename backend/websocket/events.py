"""
WebSocket Events - Real-time communication handlers
"""
import logging

logger = logging.getLogger(__name__)


def init_websocket_events(socketio, bot_state):
    """
    Initialize WebSocket event handlers
    
    Args:
        socketio: SocketIO instance
        bot_state: Bot state dictionary
    """
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        logger.info('Client connected')
        socketio.emit('status', bot_state)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info('Client disconnected')
    
    @socketio.on('start_bot')
    def handle_start_bot(data):
        """Start the bot with specific configuration"""
        logger.info(f'Starting bot with config: {data}')
        bot_state['running'] = True
        bot_state['mode'] = data.get('mode', 'manual')
        socketio.emit('bot_started', bot_state, broadcast=True)
    
    @socketio.on('stop_bot')
    def handle_stop_bot():
        """Stop the bot"""
        logger.info('Stopping bot')
        bot_state['running'] = False
        bot_state['mode'] = 'idle'
        socketio.emit('bot_stopped', bot_state, broadcast=True)

