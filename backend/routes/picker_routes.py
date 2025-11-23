"""
Picker Routes - Desktop pixel picker operations
"""
from flask import Blueprint, jsonify
import logging
import subprocess
import sys
import os
from config import Config

logger = logging.getLogger(__name__)

picker_bp = Blueprint('picker', __name__, url_prefix='/api/picker')


@picker_bp.route('/launch', methods=['POST'])
def launch_picker():
    """Launch the desktop pixel picker overlay"""
    try:
        logger.info("Launching desktop pixel picker...")
        
        # Run desktop_picker.py as a subprocess
        picker_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'desktop_picker.py')
        python_exe = sys.executable
        
        # Start picker in a new process
        process = subprocess.Popen(
            [python_exe, picker_path, '--pick'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for it to complete and get the result
        stdout, stderr = process.communicate(timeout=Config.PICKER_TIMEOUT)
        
        if process.returncode == 0:
            # Parse the output to get picked pixel data
            output = stdout.decode('utf-8')
            logger.info(f"Picker output: {output}")
            
            return jsonify({
                'success': True,
                'message': 'Pixel picker completed',
                'output': output
            })
        else:
            error = stderr.decode('utf-8')
            logger.error(f"Picker failed: {error}")
            return jsonify({
                'success': False,
                'error': error
            }), 500
            
    except subprocess.TimeoutExpired:
        process.kill()
        return jsonify({
            'success': False,
            'error': f'Picker timeout - took longer than {Config.PICKER_TIMEOUT} seconds'
        }), 500
    except Exception as e:
        logger.error(f"Exception in launch_picker: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

