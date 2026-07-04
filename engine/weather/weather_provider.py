import requests
import os
from typing import Optional, Dict

from ..utils.helpers import read_json_file
from .weather_models import CurrentWeather

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))

def _load_config() -> Dict:
    cfg = read_json_file(CONFIG_PATH)
    return cfg.get('weather', {})

def _build_url(lat: float, lon: float, api_key: str, units: str) -> str:
    return (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    )

def _build_city_url(city: str, api_key: str, units: str) -> str:
    return (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    )

def fetch_weather_by_coords(lat: float, lon: float) -> Optional[CurrentWeather]:
    cfg = _load_config()
    api_key = cfg.get('api_key')
    units = cfg.get('units', 'metric')
    if not api_key:
        return None
    try:
        resp = requests.get(_build_url(lat, lon, api_key, units), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return _parse_response(data)
    except Exception:
        return None

def fetch_weather_by_city(city: str) -> Optional[CurrentWeather]:
    cfg = _load_config()
    api_key = cfg.get('api_key')
    units = cfg.get('units', 'metric')
    if not api_key:
        return None
    try:
        resp = requests.get(_build_city_url(city, api_key, units), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return _parse_response(data)
    except Exception:
        return None

def _parse_response(data: dict) -> Optional[CurrentWeather]:
    try:
        main = data['main']
        wind = data.get('wind', {})
        sys = data.get('sys', {})
        weather = data['weather'][0] if data.get('weather') else {}
        return CurrentWeather(
            temperature=main.get('temp'),
            feels_like=main.get('feels_like'),
            humidity=main.get('humidity'),
            pressure=main.get('pressure'),
            visibility=data.get('visibility'),
            wind_speed=wind.get('speed'),
            wind_deg=wind.get('deg'),
            clouds=data.get('clouds', {}).get('all'),
            sunrise=sys.get('sunrise'),
            sunset=sys.get('sunset'),
            description=weather.get('description'),
            icon=weather.get('icon'),
            timezone=data.get('timezone'),
            city=data.get('name'),
            country=sys.get('country')
        )
    except Exception:
        return None
