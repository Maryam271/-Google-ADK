"""
Single LlmAgent — weather assistant with LIVE global weather data.

Uses Open-Meteo (free, no API key required):
  - Geocoding API  -> resolves ANY city name worldwide to lat/lon
  - Forecast API   -> returns current, accurate weather for those coordinates

Run: adk web  →  pick "single_agent"
Ask: "What's the weather in Stockholm?" / "Weather in Multan?" / "How's it in Ushuaia?"
"""
import requests
from google.adk.agents import LlmAgent

MODEL = "gemini-2.5-flash-lite"

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes -> human-readable text
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather(city: str) -> dict:
    """Retrieves the current, real-time weather for any city worldwide.

    Looks up the city via a global geocoding service to resolve its
    coordinates (so it works for major and minor cities in any country),
    then fetches live current-conditions data for that location.

    Args:
        city: The city name to look up (e.g. "Karachi", "Sao Paulo",
              "Multan, Pakistan"). Country name is optional but helps
              disambiguate cities that share a name.

    Returns:
        dict: status and result or error message.
    """
    try:
        # Step 1: Resolve city name -> lat/lon via geocoding
        geo_resp = requests.get(
            GEOCODE_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        results = geo_data.get("results")
        if not results:
            return {
                "status": "error",
                "error_message": f"Could not find a location matching '{city}'.",
            }

        place = results[0]
        lat = place["latitude"]
        lon = place["longitude"]
        resolved_name = place.get("name", city)
        country = place.get("country", "")
        admin1 = place.get("admin1", "")  # state/province

        # Step 2: Fetch live current weather for those coordinates
        weather_resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                           "weather_code,wind_speed_10m,wind_direction_10m,is_day",
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_resp.raise_for_status()
        current = weather_resp.json().get("current", {})

        if not current:
            return {
                "status": "error",
                "error_message": f"Weather data unavailable for '{city}' right now.",
            }

        code = current.get("weather_code")
        condition = WMO_CODES.get(code, "Unknown conditions")
        temp = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")

        location_label = ", ".join(p for p in [resolved_name, admin1, country] if p)

        report = (
            f"{condition}, {temp}°C (feels like {feels_like}°C) in {location_label}. "
            f"Humidity: {humidity}%, Wind: {wind} km/h."
        )

        return {
            "status": "success",
            "report": report,
            "location": location_label,
            "temperature_c": temp,
            "condition": condition,
            "humidity_pct": humidity,
            "wind_kmh": wind,
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Network error fetching weather for '{city}': {e}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error looking up '{city}': {e}",
        }


root_agent = LlmAgent(
    name="SingleAgent",
    model=MODEL,
    description="A weather assistant that looks up live, accurate current conditions "
                "for any city in any country worldwide.",
    instruction=(
        "You help users check the weather for cities anywhere in the world. "
        "Always use the get_weather tool to look up live conditions for any city "
        "they ask about — never guess or make up weather data. "
        "If the city name is ambiguous (e.g. there are multiple cities with that name "
        "in different countries), ask the user to clarify the country, or pass the "
        "city with country appended (e.g. 'Multan, Pakistan') to the tool. "
        "If the tool returns an error, tell the user clearly and suggest they check "
        "the spelling or add the country name."
    ),
    tools=[get_weather],
)