"""
engine/commands/app_commands.py
Utilities for launching and controlling installed applications on Windows.
"""

import subprocess
import os
import sys
from pathlib import Path
from engine.ui.logs import logger

# A small registry of common apps – users can extend via config.json if desired.
APP_REGISTRY = {
    "notepad": "notepad.exe",
    "calc": "calc.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "vscode": "Code.exe",
    "visualstudio": "devenv.exe",
    "slack": "slack.exe",
    "discord": "Discord.exe",
    "spotify": "Spotify.exe",
    "explorer": "explorer.exe",
    "terminal": "wt.exe",  # Windows Terminal
}


def _resolve_executable(app_name: str) -> str | None:
    """Return a full path to the executable if it exists.
    First checks the APP_REGISTRY for a known executable name.
    If not found in PATH, falls back to scanning Start‑Menu shortcuts via
    :func:`engine.system.installed_apps.find_app`.
    """
    exe = APP_REGISTRY.get(app_name.lower())
    if exe:
        # Direct absolute path?
        if os.path.isabs(exe) and Path(exe).exists():
            return exe
        # Search system PATH
        for dir in os.getenv("PATH", "").split(os.pathsep):
            candidate = Path(dir) / exe
            if candidate.exists():
                return str(candidate)
                
    # Fallback: look for a shortcut in the cached installed apps
    try:
        from engine.system.installed_apps import find_app
        shortcut = find_app(app_name)
        if shortcut:
            return shortcut
    except Exception:
        pass
    return None


def launch_app(app_name: str) -> str:
    """Launch an application by its friendly name.
    Returns a user‑friendly status string.
    """
    exe_path = _resolve_executable(app_name)
    if not exe_path:
        logger.log(f"App launch failed – unknown app '{app_name}'.", "WARN")
        return f"I could not locate the application '{app_name}' on your system."
    try:
        if hasattr(os, 'startfile'):
            os.startfile(exe_path)
        else:
            subprocess.Popen([exe_path], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.log(f"Launched application: {app_name} ({exe_path})", "OK")
        return f"Launching {app_name} now."
    except Exception as e:
        logger.log(f"Failed to launch {app_name}: {e}", "ERROR")
        return f"I tried to start {app_name}, but something went wrong: {e}."


def close_app(app_name: str) -> str:
    """Terminate a running process by name.
    Uses Windows taskkill for simplicity.
    """
    exe = APP_REGISTRY.get(app_name.lower())
    if not exe:
        return f"I don't have a known process name for '{app_name}'."
    try:
        subprocess.run(["taskkill", "/F", "/IM", exe], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.log(f"Closed application: {app_name} ({exe})", "OK")
        return f"{app_name} has been terminated."
    except subprocess.CalledProcessError:
        return f"I couldn't find a running instance of {app_name}."
    except Exception as e:
        logger.log(f"Error closing {app_name}: {e}", "ERROR")
        return f"Failed to close {app_name}: {e}."
