import json
import os
import platform
import subprocess
from typing import Optional

import requests

from ..utils.helpers import read_json_file

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'))

def _get_location_from_windows() -> Optional[dict]:
    """Attempt to retrieve location via Windows Location API using PowerShell.
    Returns a dict with latitude, longitude, city, state, country if successful.
    """
    if platform.system() != "Windows":
        return None
    try:
        # PowerShell command to get GeoCoordinate via Windows.Devices.Geolocation
        ps_script = """
        Add-Type -AssemblyName System.Device
        $geo = [System.Device.Location.GeoCoordinateWatcher]::new()
        $geo.Start()
        Start-Sleep -Milliseconds 500
        $coord = $geo.Position.Location
        $lat = $coord.Latitude
        $lon = $coord.Longitude
        if ($lat -and $lon) {
            $city = ''
            $state = ''
            $country = ''
            Write-Output ("{\"latitude\":$lat,\"longitude\":$lon,\"city\":\"\",\"state\":\"\",\"country\":\"\"}")
        }
        """
        result = subprocess.check_output(['powershell', '-Command', ps_script], text=True)
        data = json.loads(result.strip())
        return data
    except Exception:
        return None

def _get_location_from_ip() -> Optional[dict]:
    """Fallback to IP‑based geolocation using ip-api.com (no API key required)."""
    try:
        resp = requests.get('http://ip-api.com/json/', timeout=5)
        if resp.status_code == 200:
            d = resp.json()
            return {
                "latitude": d.get('lat'),
                "longitude": d.get('lon'),
                "city": d.get('city'),
                "state": d.get('regionName'),
                "country": d.get('country')
            }
    except Exception:
        return None
    return None

def _get_location_from_config() -> Optional[dict]:
    """Final fallback to the default city defined in config.json.
    Coordinates are set to 0; the weather provider will resolve the city name.
    """
    cfg = read_json_file(CONFIG_PATH)
    city = cfg.get('weather', {}).get('default_city', 'Rourkela')
    return {
        "latitude": 0.0,
        "longitude": 0.0,
        "city": city,
        "state": None,
        "country": None
    }

def detect_location() -> dict:
    """Detect user location following priority:
    1. Windows location services
    2. IP geolocation
    3. Config default city
    Returns a dict with keys: latitude, longitude, city, state, country.
    """
    loc = _get_location_from_windows()
    if loc and loc.get('latitude') and loc.get('longitude'):
        return loc
    loc = _get_location_from_ip()
    if loc and loc.get('latitude') and loc.get('longitude'):
        return loc
    return _get_location_from_config()
