import eel
import os
import sys
import traceback

# Ensure the working directory is the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(PROJECT_ROOT)

# Add engine package to path
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'engine'))

# Import core components
from engine.core.config import load_config
from engine.ui.ui_controller import UIController, register_command_handler
from engine.core.startup import run_startup_diagnostics
from engine.eel.eel_manager import init_eel
from engine.commands.command_handler import CommandHandler

# Load configuration
config = load_config()

# Initialize UI controller with Eel
ui = UIController(config)

# Run startup diagnostics (logs to UI)
run_startup_diagnostics(ui)

# Initialize Eel and start the UI
if not init_eel(debug=False, size=(1280, 720), fullscreen=False):
    ui.log("Failed to initialize Eel UI.", level="ERROR")
    sys.exit(1)
# Initialize command handling
handler = CommandHandler()
register_command_handler(handler)

# Start the UI (index.html) with desired size and        # UI already started by init_eel (init_eel handles server)

# Keep the script alive while Eel runs
while True:
    try:
        eel.sleep(1.0)
    except KeyboardInterrupt:
        break
    except Exception as e:
        ui.log(f"Unexpected error in main loop: {e}", level="ERROR")
        traceback.print_exc()
        break
