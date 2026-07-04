from .weather_models import CurrentWeather


def format_for_ui(weather: CurrentWeather) -> dict:
    """Convert CurrentWeather dataclass into a plain dict suitable for the frontend.
    Keys match the IDs expected in the HTML weather panel.
    """
    if not weather:
        return {}
    return {
        "city": weather.city,
        "country": weather.country,
        "temperature": round(weather.temperature, 1) if weather.temperature is not None else None,
        "feels_like": round(weather.feels_like, 1) if weather.feels_like is not None else None,
        "humidity": weather.humidity,
        "pressure": weather.pressure,
        "visibility": weather.visibility,
        "wind_speed": round(weather.wind_speed, 1) if weather.wind_speed is not None else None,
        "wind_deg": weather.wind_deg,
        "clouds": weather.clouds,
        "sunrise": weather.sunrise,
        "sunset": weather.sunset,
        "description": weather.description.title() if weather.description else "",
        "icon": weather.icon,
        "last_updated": None  # filled by service
    }


def format_for_voice(weather: CurrentWeather) -> str:
    """Create a natural‑language sentence for voice output."""
    if not weather:
        return "Sorry, I could not retrieve the weather information."
    parts = []
    location = f"in {weather.city}" if weather.city else ""
    parts.append(f"Currently {location} it is {round(weather.temperature)} degrees Celsius")
    if weather.description:
        parts.append(f"with {weather.description.lower()}")
    if weather.humidity is not None:
        parts.append(f"humidity is {weather.humidity} percent")
    if weather.wind_speed is not None:
        parts.append(f"wind speed is {round(weather.wind_speed)} kilometers per hour")
    return ", ".join(parts) + "."
