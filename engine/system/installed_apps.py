// engine/system/installed_apps.py
"""Utility to scan Windows Start Menu for installed applications.
Creates a JSON cache at data/installed_apps.json for quick lookup.
"""
import os
import json
import pathlib
from typing import Dict

CACHE_PATH = pathlib.Path(__file__).resolve().parents[2] / "data" / "installed_apps.json"

def _scan_start_menu() -> Dict[str, str]:
    """Scan common Start‑Menu locations for .lnk shortcuts.
    Returns a mapping of *app name* → *executable path*.
    """
    shortcuts = {}
    start_dirs = [
        pathlib.Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        pathlib.Path(os.getenv("PROGRAMDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    ]
    for start_dir in start_dirs:
        if not start_dir.is_dir():
            continue
        for root, _, files in os.walk(start_dir):
            for f in files:
                if f.lower().endswith('.lnk'):
                    name = pathlib.Path(f).stem.lower()
                    target = pathlib.Path(root) / f
                    shortcuts[name] = str(target)
    return shortcuts

def load_app_cache() -> Dict[str, str]:
    """Load the cached app mapping, rescanning if the cache is missing or stale."""
    if CACHE_PATH.is_file():
        try:
            with open(CACHE_PATH, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        except Exception:
            pass
    # Cache miss or corrupt – rebuild
    apps = _scan_start_menu()
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, 'w', encoding='utf-8') as fp:
        json.dump(apps, fp, indent=2)
    return apps

def find_app(app_name: str) -> str | None:
    """Return the executable path for *app_name* (case‑insensitive fuzzy match)."""
    apps = load_app_cache()
    key = app_name.lower()
    if key in apps:
        return apps[key]
    # Simple fuzzy fallback – contains
    for name, path in apps.items():
        if key in name:
            return path
    return None
