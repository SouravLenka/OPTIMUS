# engine/core/shutdown.py
"""Graceful shutdown utilities for OPTIMUS.

This module provides a single ``run_cleanup`` function that is invoked when the
application receives a termination signal (SIGINT/SIGTERM) or when the UI calls
``close_app``.  The current implementation performs minimal cleanup – it
flushes pending logs and ensures any background threads are stopped.  Additional
cleanup steps (e.g., releasing microphone resources) can be added later.
"""
import threading
import logging

# Obtain the global logger from the UI logger module if it exists; otherwise
# fall back to a basic configuration.
try:
    from engine.ui.logs import logger as ui_logger
except Exception:
    ui_logger = None
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("optimum.shutdown")
else:
    logger = ui_logger

def _stop_background_threads():
    """Placeholder for stopping any background threads.

    The project currently does not spawn long‑running threads besides the Eel UI
    loop, which is terminated by ``close_app``.  This function exists for future
    extensibility.
    """
    # Example: if you have a thread pool or async loop, shut it down here.
    pass

def run_cleanup() -> None:
    """Execute cleanup actions before the process exits.

    - Log the shutdown event.
    - Stop background threads.
    - Flush log handlers.
    """
    logger.info("[SHUTDOWN] Running cleanup routine")
    _stop_background_threads()
    # Flush any pending logs
    for handler in logger.handlers:
        handler.flush()
    logger.info("[SHUTDOWN] Cleanup complete")
