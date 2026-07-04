import dataclasses
from typing import Optional

@dataclasses.dataclass
class Location:
    latitude: float
    longitude: float
    city: str
    state: Optional[str] = None
    country: str = ""

@dataclasses.dataclass
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    visibility: int
    wind_speed: float
    wind_deg: int
    clouds: int
    sunrise: int
    sunset: int
    description: str
    icon: str
    timezone: int
    city: str
    country: str
