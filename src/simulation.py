"""
simulation.py  –  Offline simulation mode using sample_weather.json
"""
import json, os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sample_weather.json")

def load_data() -> dict:
    with open(DATA_FILE, "r") as f:
        return json.load(f)["cities"]

def get_available_cities() -> list:
    return list(load_data().keys())

def fetch_simulated_current(city: str) -> dict:
    """Return simulated current weather for a city."""
    data = load_data()
    city_key = _find_city(city, data)
    raw = data[city_key]["current"]
    return {
        "city": city_key, "country": "SIM",
        "temp": raw["temp"], "feels_like": raw["feels_like"],
        "temp_min": raw["temp"] - 3, "temp_max": raw["temp"] + 2,
        "humidity": raw["humidity"], "pressure": raw["pressure"],
        "wind_speed": raw["wind_speed"], "wind_deg": raw["wind_deg"],
        "description": raw["description"],
        "visibility": raw.get("visibility", 5000),
        "sunrise": "06:15", "sunset": "18:45",
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "SIMULATION"
    }

def fetch_simulated_forecast(city: str) -> list:
    """Return simulated 5-day forecast."""
    data = load_data()
    city_key = _find_city(city, data)
    return data[city_key]["forecast"]

def _find_city(city: str, data: dict) -> str:
    """Case-insensitive city lookup."""
    for key in data:
        if key.lower() == city.lower():
            return key
    available = ", ".join(data.keys())
    raise ValueError(
        f"City '{city}' not in simulation data.\n"
        f"Available cities: {available}"
    )
