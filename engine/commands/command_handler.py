"""
engine/commands/command_handler.py
Central routing of natural‑language commands to subsystem modules.
"""

import re
from typing import Callable, Dict

from engine.commands.system_commands import (
    get_time,
    get_date,
    get_battery,
    get_cpu_ram,
    get_disk_usage,
    get_full_diagnostics,
    get_ip_address,
)
from engine.commands.web_commands import (
    open_website,
    open_url,
    google_search,
    youtube_search,
    youtube_play,
)
from engine.commands.app_commands import launch_app, close_app

# Map of simple regex patterns to handler callables.
# The order matters – first match wins.
PATTERN_HANDLERS: list[tuple[re.Pattern, Callable[[re.Match], str]]] = [
    # System queries
    (re.compile(r"\btime\b", re.I), lambda _: get_time()),
    (re.compile(r"\bdate\b", re.I), lambda _: get_date()),
    (re.compile(r"\bbattery\b", re.I), lambda _: get_battery()),
    (re.compile(r"\bcpu|\bprocessor\b", re.I), lambda _: get_cpu_ram()),
    (re.compile(r"\bram|\bmemory\b", re.I), lambda _: get_cpu_ram()),
    (re.compile(r"\bdisk|\bstorage\b", re.I), lambda _: get_disk_usage()),
    (re.compile(r"\bdiagnostic|\bstatus\b", re.I), lambda _: get_full_diagnostics()),
    (re.compile(r"\bip\s*address\b", re.I), lambda _: get_ip_address()),
    # Web actions
    (re.compile(r"open\s+(?P<site>\w+)", re.I), lambda m: open_website(m.group("site"))),
    (re.compile(r"open\s+url\s+(?P<url>https?://\S+)", re.I), lambda m: open_url(m.group("url"))),
    (re.compile(r"search\s+google\s+for\s+(?P<q>.+)", re.I), lambda m: google_search(m.group("q"))),
    (re.compile(r"search\s+youtube\s+for\s+(?P<q>.+)", re.I), lambda m: youtube_search(m.group("q"))),
    (re.compile(r"play\s+(?P<q>.+?)(?:\s+on\s+youtube)?$", re.I), lambda m: youtube_play(m.group("q"))),
    # Application control
    (re.compile(r"launch\s+(?P<app>\w+)", re.I), lambda m: launch_app(m.group("app"))),
    (re.compile(r"open\s+(?P<app>\w+)", re.I), lambda m: launch_app(m.group("app"))),
    (re.compile(r"close\s+(?P<app>\w+)", re.I), lambda m: close_app(m.group("app")))
]

# --------------------------------------------------------------------------
# Command handler wrapper
# --------------------------------------------------------------------------

class CommandHandler:
    """Thin wrapper exposing a process_command method for UI integration.

    The backend UI controller expects an object with a ``process_command`` method.
    This class forwards the call to the module‑level ``handle_command`` function.
    """

    def process_command(self, command: str) -> str:
        """Process *command* using the existing routing logic.

        Returns the response string that can be spoken or displayed.
        """
        return handle_command(command)




def handle_command(command: str) -> str:
    """Parse *command* and dispatch to the appropriate subsystem.
    Returns a human‑readable response that can be spoken back to the user.
    """
    command = command.strip()
    if not command:
        return "I didn't catch that. Please say a command."

    for pattern, handler in PATTERN_HANDLERS:
        match = pattern.search(command)
        if match:
            try:
                return handler(match)
            except Exception as e:
                return f"An error occurred while processing your request: {e}"

    # Fallback – unknown intent
    return "I'm not sure how to handle that request yet. You can ask me about the time, open a website, or launch an application."

# Export a simple dictionary for UI binding (optional) – allows the frontend to call via Eel.
COMMANDS: Dict[str, Callable[[str], str]] = {"handle": handle_command}
