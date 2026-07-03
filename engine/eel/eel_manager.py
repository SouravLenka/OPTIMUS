# engine/eel/eel_manager.py
"""Eel manager for initializing and managing the Eel UI server.
Provides a clean API for main.py and other components to start the UI,
expose backend callbacks, and safely invoke JavaScript functions.
"""

import sys
import threading
from pathlib import Path
import eel

# Determine project root (two levels up from this file) and web folder path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_ROOT = PROJECT_ROOT / "web"

# Event flag indicating that the frontend has signaled readiness
_frontend_ready_event = threading.Event()

def init_eel(debug: bool = False, size: tuple = (1280, 720), fullscreen: bool = False) -> bool:
    """Initialize the Eel server.

    Args:
        debug: Launch with Chrome devtools if True.
        size: Window size (width, height).
        fullscreen: Open the UI in fullscreen mode.

    Returns:
        True if the frontend reported readiness within the timeout.
    """
    if not WEB_ROOT.is_dir():
        raise FileNotFoundError(f"Web folder not found at {WEB_ROOT}")

    eel.init(str(WEB_ROOT))

    @eel.expose
    def _frontend_ready():
        """Called from JavaScript once the UI has loaded."""
        _frontend_ready_event.set()
        return "ready"

    def _run():
        # block=False makes eel.start non‑blocking; we keep the thread alive.
        eel.start('index.html', size=size, mode='chrome', block=False, port=0)
        while True:
            try:
                eel.sleep(1)
            except KeyboardInterrupt:
                break

    threading.Thread(target=_run, daemon=True).start()
    _frontend_ready_event.wait(timeout=5)
    return _frontend_ready_event.is_set()

def expose(name: str):
    """Decorator to expose a Python function to the frontend."""
    def decorator(func):
        eel.expose(func)
        return func
    return decorator

def call_js(func_name: str, *args, **kwargs):
    """Safely invoke a JavaScript function exposed via Eel."""
    try:
        js_func = getattr(eel, func_name)
        js_func(*args, **kwargs)()
    except Exception:
        pass

@eel.expose
def close_app():
    """Close the application from the frontend."""
    sys.exit(0)
