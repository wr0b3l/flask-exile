"""
Monitor Routes - CRUD operations for monitors
"""
from flask import Blueprint, jsonify, request
import logging

logger = logging.getLogger(__name__)

monitor_bp = Blueprint('monitor', __name__, url_prefix='/api/monitor')


def init_monitor_routes(monitor_service, persistence_service, monitoring_loop, socketio):
    """
    Initialize monitor routes with dependencies
    
    Args:
        monitor_service: MonitorService instance
        persistence_service: PersistenceService instance
        monitoring_loop: MonitoringLoop instance
        socketio: SocketIO instance
    """
    
    @monitor_bp.route('/list', methods=['GET'])
    def list_monitors():
        """List all pixel monitors"""
        monitors = monitor_service.get_all()
        
        # Create clean monitors with active states
        clean_monitors = []
        for monitor in monitors:
            clean_monitor = {
                'id': monitor['id'],
                'name': monitor['name'],
                'x': monitor['x'],
                'y': monitor['y'],
                'target_color': monitor['target_color'],
                'tolerance': monitor['tolerance'],
                'cooldown': monitor.get('cooldown', 1000),
                'action': monitor['action'],
                'enabled': monitor['enabled'],
                'in_cooldown': monitor.get('in_cooldown', False),
                'blocked_by_master': monitor.get('blocked_by_master', False),
                'monitor_type': monitor.get('monitor_type', 'normal'),
                'master_id': monitor.get('master_id', None),
                'trigger_mode': monitor.get('trigger_mode', 'no_match'),
                'pixel_group': monitor.get('pixel_group', []),
                'group_logic': monitor.get('group_logic', 'all_match'),
                'is_active': monitor.get('_last_active_state', False)
            }
            clean_monitors.append(clean_monitor)
        
        return jsonify({
            'success': True,
            'monitors': clean_monitors,
            'count': len(clean_monitors)
        })
    
    @monitor_bp.route('/add', methods=['POST'])
    def add_monitor():
        """Add a new pixel monitor"""
        try:
            data = request.get_json() or {}
            
            required_fields = ['x', 'y', 'target_color', 'action']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }), 400
            
            # Add monitor via service
            success, message, monitor = monitor_service.add(data)
            
            if not success:
                return jsonify({'success': False, 'error': message}), 400
            
            # Save to file
            persistence_service.save_monitors(monitor_service.get_all())
            
            # Start monitoring thread if not already running
            monitoring_loop.start()
            
            # Emit update to all connected clients
            socketio.emit('monitor_added', monitor)
            
            # Emit log message
            socketio.emit('activity_log', {
                'type': 'success',
                'message': f"Monitor '{monitor['name']}' added at ({monitor['x']}, {monitor['y']})"
            })
            
            return jsonify({
                'success': True,
                'monitor': monitor
            })
            
        except Exception as e:
            logger.error(f"Exception in add_monitor: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @monitor_bp.route('/edit/<int:monitor_id>', methods=['PUT'])
    def edit_monitor(monitor_id):
        """Edit an existing pixel monitor"""
        try:
            data = request.get_json() or {}
            
            success, message, monitor = monitor_service.update(monitor_id, data)
            
            if not success:
                status_code = 404 if 'not found' in message else 400
                return jsonify({'success': False, 'error': message}), status_code
            
            # Save to file
            persistence_service.save_monitors(monitor_service.get_all())
            
            # Create clean monitor for emission (no datetime objects)
            clean_monitor = {
                'id': monitor['id'],
                'name': monitor['name'],
                'x': monitor['x'],
                'y': monitor['y'],
                'target_color': monitor['target_color'],
                'tolerance': monitor['tolerance'],
                'cooldown': monitor.get('cooldown', 1000),
                'action': monitor['action'],
                'enabled': monitor['enabled'],
                'in_cooldown': monitor.get('in_cooldown', False),
                'blocked_by_master': monitor.get('blocked_by_master', False),
                'monitor_type': monitor.get('monitor_type', 'normal'),
                'master_id': monitor.get('master_id', None),
                'trigger_mode': monitor.get('trigger_mode', 'no_match')
            }
            
            # Emit update to all connected clients
            socketio.emit('monitor_updated', clean_monitor)
            
            # Emit log message
            socketio.emit('activity_log', {
                'type': 'info',
                'message': f"Monitor '{monitor['name']}' edited"
            })
            
            return jsonify({
                'success': True,
                'monitor': clean_monitor
            })
            
        except Exception as e:
            logger.error(f"Exception in edit_monitor: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @monitor_bp.route('/toggle/<int:monitor_id>', methods=['POST'])
    def toggle_monitor(monitor_id):
        """Enable/disable (pause/resume) a pixel monitor"""
        try:
            success, status, monitor = monitor_service.toggle(monitor_id)
            
            if not success:
                return jsonify({'success': False, 'error': status}), 404
            
            # Save to file
            persistence_service.save_monitors(monitor_service.get_all())
            
            # Create clean monitor for emission
            clean_monitor = {
                'id': monitor['id'],
                'name': monitor['name'],
                'x': monitor['x'],
                'y': monitor['y'],
                'target_color': monitor['target_color'],
                'tolerance': monitor['tolerance'],
                'cooldown': monitor.get('cooldown', 1000),
                'action': monitor['action'],
                'enabled': monitor['enabled'],
                'in_cooldown': monitor.get('in_cooldown', False),
                'blocked_by_master': monitor.get('blocked_by_master', False),
                'monitor_type': monitor.get('monitor_type', 'normal'),
                'master_id': monitor.get('master_id', None),
                'trigger_mode': monitor.get('trigger_mode', 'no_match')
            }
            
            # Emit update to all connected clients
            socketio.emit('monitor_updated', clean_monitor)
            
            # Emit log message
            log_type = 'success' if monitor['enabled'] else 'warning'
            socketio.emit('activity_log', {
                'type': log_type,
                'message': f"Monitor '{monitor['name']}' {status}"
            })
            
            return jsonify({
                'success': True,
                'monitor': clean_monitor,
                'status': status
            })
            
        except Exception as e:
            logger.error(f"Exception in toggle_monitor: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @monitor_bp.route('/remove/<int:monitor_id>', methods=['DELETE'])
    def remove_monitor(monitor_id):
        """Remove a pixel monitor"""
        try:
            success, message, monitor_name = monitor_service.remove(monitor_id)
            
            if not success:
                return jsonify({'success': False, 'error': message}), 404
            
            # Save to file
            persistence_service.save_monitors(monitor_service.get_all())
            
            # Stop monitoring if no monitors left
            if monitor_service.count() == 0:
                monitoring_loop.stop()
            
            # Emit update to all connected clients
            socketio.emit('monitor_removed', {'id': monitor_id})
            
            # Emit log message
            socketio.emit('activity_log', {
                'type': 'warning',
                'message': f"Monitor '{monitor_name}' removed"
            })
            
            return jsonify({
                'success': True,
                'message': f'Monitor {monitor_id} removed'
            })
            
        except Exception as e:
            logger.error(f"Exception in remove_monitor: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return monitor_bp

