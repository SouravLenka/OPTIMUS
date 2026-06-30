import sys
import os
import traceback
import signal

# Ensure the working directory is the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(PROJECT_ROOT)

# Add engine package to path
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'engine'))

# Import core components
from engine.core.config import load_config
from engine.ui.ui_controller import UIController
from engine.core.startup import run_startup_diagnostics
from engine.eel.eel_manager import init_eel, close_app  # expose close_app to frontend
from engine.core.shutdown import run_cleanup

# Load configuration
config = load_config()

# Initialize UI controller with Eel (provides logging etc.)
ui = UIController(config)

# Run startup diagnostics (logs to UI)
run_startup_diagnostics(ui)

# Initialize Eel and start UI
web_path = os.path.join(PROJECT_ROOT, 'web')
if not init_eel(debug=False, size=(1280, 720), fullscreen=False):
    ui.log("Failed to initialize Eel UI.", level="ERROR")
    sys.exit(1)

# Register signal handlers for graceful termination (Ctrl+C, termination)
def handle_exit(signum, frame):
    ui.log("Received termination signal, shutting down...", level="SYS")
    run_cleanup()
    sys.exit(0)

for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, handle_exit)

# Keep the script alive while Eel runs – the frontend will call close_app() on window close
try:
    while True:
        # The backend loop is essentially idle; Eel maintains its own event loop.
        # Sleep a short interval to keep the process responsive to signals.
        import time
        time.sleep(1)
except KeyboardInterrupt:
    handle_exit(None, None)

# Ensure cleanup in case the loop exits unexpectedly
run_cleanup()
