"""
Pixel Bot - Development Server Launcher
Starts the Flask backend with the integrated dashboard
"""

import subprocess
import sys
import os
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(prefix, message, color=Colors.ENDC):
    """Print log message with timestamp and prefix"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{color}[{timestamp}] [{prefix}]{Colors.ENDC} {message}")

def main():
    """Main function to start the backend server"""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("=" * 60)
    print("       PIXEL BOT - DEVELOPMENT SERVER")
    print("=" * 60)
    print(f"{Colors.ENDC}")
    print()
    
    # Check if backend exists
    if not os.path.exists('backend'):
        log("ERROR", "Backend directory not found!", Colors.RED)
        return 1
    
    # Check if virtual environment exists
    venv_python = os.path.join('backend', 'venv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        venv_python = os.path.join('backend', 'venv', 'bin', 'python')  # Unix
    
    if not os.path.exists(venv_python):
        log("ERROR", "Virtual environment not found!", Colors.RED)
        log("ERROR", "Please run: cd backend && python -m venv venv && pip install -r requirements.txt", Colors.YELLOW)
        return 1
    
    log("SYSTEM", "Dependencies OK", Colors.GREEN)
    print()
    
    # Start backend server
    log("BACKEND", "Starting Flask server with integrated dashboard...", Colors.CYAN)
    print()
    
    try:
        process = subprocess.Popen(
            [venv_python, os.path.join('backend', 'app.py')],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print(f"{Colors.BOLD}{Colors.GREEN}")
        print("=" * 60)
        print("       APPLICATION RUNNING!")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        print(f"{Colors.YELLOW}Dashboard: http://localhost:5000{Colors.ENDC}")
        print(f"{Colors.YELLOW}API:       http://localhost:5000/api/status{Colors.ENDC}")
        print()
        print(f"{Colors.BOLD}Press Ctrl+C to stop the server{Colors.ENDC}")
        print("=" * 60)
        print()
        
        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                log("BACKEND", line.strip(), Colors.BLUE)
        
        process.wait()
        
    except KeyboardInterrupt:
        print()
        log("SYSTEM", "Shutting down server...", Colors.YELLOW)
        process.terminate()
        process.wait()
        print()
        log("SYSTEM", "Server stopped", Colors.GREEN)
        return 0
    except Exception as e:
        log("ERROR", f"Server error: {e}", Colors.RED)
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        log("SYSTEM", "Goodbye!", Colors.GREEN)
        sys.exit(0)
