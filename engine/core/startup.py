import traceback
from engine.ui.ui_controller import UIController
from engine.core.assistant_state import AssistantState, state_manager
from engine.core.config import config

def run_startup_diagnostics(ui: UIController) -> None:
    """Run basic startup checks and log results to the UI.

    * Verifies configuration loading
    * Checks assistant state transitions
    * Logs system information (OS, Python version)
    """
    try:
        ui.log("🚀 Starting OPTIMUS diagnostics...", level="OK")
        # Log configuration summary
        ui.log(f"Configuration loaded: {config.settings}", level="SYS")
        # Log environment info
        import platform, sys
        ui.log(f"Python {sys.version.split(' ')[0]} on {platform.system()} {platform.release()}", level="SYS")
        # Verify state machine can transition
        state_manager.set_state(AssistantState.IDLE)
        ui.log(f"Assistant state set to {state_manager.get_state().name}", level="OK")
    except Exception as e:
        ui.log(f"❗ Startup diagnostics failed: {e}", level="ERROR")
        traceback.print_exc()
