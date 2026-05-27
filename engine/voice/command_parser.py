import re
import json
from enum import Enum
from typing import Dict, Any

class Intent(Enum):
    OPEN_APP = "open_app"
    SEARCH_WEB = "search_web"
    TAKE_SCREENSHOT = "screenshot"
    PLAY_MEDIA = "play_media"
    UNKNOWN = "unknown"

# Simple pattern map – can be expanded later
_PATTERNS = {
    Intent.OPEN_APP: re.compile(r"\b(open|launch|start)\s+(?P<app>.+)", re.IGNORECASE),
    Intent.SEARCH_WEB: re.compile(r"\b(search|find|lookup)\s+(?P<query>.+)", re.IGNORECASE),
    Intent.TAKE_SCREENSHOT: re.compile(r"\b(screenshot|capture screen|take a screenshot)\b", re.IGNORECASE),
    Intent.PLAY_MEDIA: re.compile(r"\b(play|pause|stop)\s+(?P<media>.+)", re.IGNORECASE),
}

def parse_command(command: str) -> Dict[str, Any]:
    """Parse a raw command string and return a dict with ``intent`` and ``params``.

    The returned ``intent`` is a member of :class:`Intent`. ``params`` contains
    the captured named groups from the matching regex, or an empty dict for
    unknown intents.
    """
    command = command.strip()
    for intent, pattern in _PATTERNS.items():
        match = pattern.search(command)
        if match:
            return {"intent": intent, "params": match.groupdict()}
    return {"intent": Intent.UNKNOWN, "params": {"raw": command}}

# Helper for debugging: dump pattern list to a JSON file (optional)
def dump_patterns(path: str = "data/command_patterns.json"):
    data = {intent.value: pat.pattern for intent, pat in _PATTERNS.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
