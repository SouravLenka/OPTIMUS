import time
from typing import Optional, Dict
from .weather_models import CurrentWeather

_cache: Dict[str, Dict] = {}

def get_cached_weather(key: str) -> Optional[CurrentWeather]:
    """Return cached weather if present and not expired.
    ``key`` is typically "current".
    """
    entry = _cache.get(key)
    if not entry:
        return None
    timestamp = entry.get('timestamp')
    data = entry.get('data')
    # Cache timeout is read from config each call
    from .weather_service import get_cache_minutes
    if time.time() - timestamp < get_cache_minutes() * 60:
        return data
    # expired
    del _cache[key]
    return None

def set_cached_weather(key: str, data: CurrentWeather) -> None:
    _cache[key] = {'timestamp': time.time(), 'data': data}
