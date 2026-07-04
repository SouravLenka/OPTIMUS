// engine/utils/helpers.py
"""Helper utilities for the OPTIMUS backend.
"""
import json
import os
from typing import Any, Dict


def to_json(data: Any, **kwargs) -> str:
    """Serialize data to a JSON string with pretty formatting.
    ``kwargs`` are passed to ``json.dumps``.
    """
    return json.dumps(data, ensure_ascii=False, indent=2, **kwargs)


def merge_dicts(base: Dict, updates: Dict) -> Dict:
    """Recursively merge ``updates`` into ``base`` and return the merged dict.
    Non‑dict values are overwritten.
    """
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = merge_dicts(base.get(key, {}), value)
        else:
            base[key] = value
    return base


def read_json_file(path: str) -> Dict:
    """Safely read a JSON file and return a dict.
    Returns an empty dict if the file does not exist or is invalid.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
