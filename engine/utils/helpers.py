// engine/utils/helpers.py
"""Helper utilities for the OPTIMUS backend.
"""
import json
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
