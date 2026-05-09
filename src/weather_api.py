"""
weather_api.py  –  Live OpenWeatherMap API integration
"""
import os, requests
from datetime import datetime
from collections import defaultdict, Counter

BASE_CURRENT  = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

def get_api_key(provided_key: str = None) -> str:
    """
    Return API key. Priority:
      1. key passed directly as argument (from Streamlit text input)
      2. OPENWEATHER_API_KEY environment variable (.env file)
    Always strips whitespace / newlines to prevent 401 errors.
    """
    key = (provided_key or os.getenv("OPENWEATHER_API_KEY", "")).strip()
    if not key:
        raise EnvironmentError(
            "No API key found.\n"
            "• Dashboard: paste your key in the sidebar API Key field.\n"
            "• CLI: add OPENWEATHER_API_KEY=your_key to your .env file.\n"
            "  Get a free key at https://openweathermap.org/api"
        )
    return key

def validate_api_key(api_key: str = None) -> dict:
    """
    Quick ping to check if the API key is valid.
    Returns {"valid": True/False, "message": str}
    """
    try:
        key = get_api_key(api_key)
        params = {"q": "London", "appid": key, "units": "metric"}
        r = requests.get(BASE_CURRENT, params=params, timeout=8)
        if r.status_code == 200:
            return {"valid": True, "message": "✅ API key is valid and working!"}
        elif r.status_code == 401:
            return {"valid": False, "message": (
                "❌ API key rejected (401 Unauthorized).\n"
                "Possible reasons:\n"
                "  • New keys take up to 2 hours to activate after account creation.\n"
                "  • Key was copied with extra spaces — make sure there are no spaces.\n"
                "  • Wrong key — check your OpenWeatherMap account dashboard.\n"
                "  • Free plan may need email verification first."
            )}
        else:
            return {"valid": False, "message": f"❌ Unexpected status: HTTP {r.status_code}"}
    except ConnectionError:
        return {"valid": False, "message": "❌ No internet connection."}
    except Exception as e:
        return {"valid": False, "message": f"❌ Error: {e}"}

def fetch_current_weather(city: str, api_key: str = None) -> dict:
    """Fetch current weather from OpenWeatherMap."""
    params = {"q": city, "appid": get_api_key(api_key), "units": "metric"}
    try:
        r = requests.get(BASE_CURRENT, params=params, timeout=10)
        r.raise_for_status()
        raw = r.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection. Use: --mode sim")
    except requests.exceptions.HTTPError:
        code = r.status_code
        if code == 401:
            raise PermissionError(
                "Invalid API key (401).\n"
                "• New keys can take up to 2 hours to activate.\n"
                "• Make sure you copied the full key with no extra spaces.\n"
                "• Verify at: https://home.openweathermap.org/api_keys"
            )
        if code == 404: raise ValueError(f"City '{city}' not found. Try a different spelling.")
        raise RuntimeError(f"HTTP {code}")
    return {
        "city":        raw.get("name", city),
        "country":     raw["sys"].get("country", "??"),
        "temp":        raw["main"]["temp"],
        "feels_like":  raw["main"]["feels_like"],
        "temp_min":    raw["main"]["temp_min"],
        "temp_max":    raw["main"]["temp_max"],
        "humidity":    raw["main"]["humidity"],
        "pressure":    raw["main"]["pressure"],
        "wind_speed":  raw["wind"]["speed"],
        "wind_deg":    raw["wind"].get("deg", 0),
        "description": raw["weather"][0]["description"],
        "visibility":  raw.get("visibility", 0),
        "sunrise":     datetime.fromtimestamp(raw["sys"]["sunrise"]).strftime("%H:%M"),
        "sunset":      datetime.fromtimestamp(raw["sys"]["sunset"]).strftime("%H:%M"),
        "fetched_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def fetch_forecast(city: str, api_key: str = None) -> list:
    """Fetch 5-day forecast aggregated into daily summaries."""
    params = {"q": city, "appid": get_api_key(api_key), "units": "metric", "cnt": 40}
    try:
        r = requests.get(BASE_FORECAST, params=params, timeout=10)
        r.raise_for_status()
        items = r.json()["list"]
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet. Use simulation mode.")
    days = defaultdict(lambda: {"temps":[],"humidity":[],"rain":0.0,"wind_speed":[],"descriptions":[]})
    for item in items:
        date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
        d = days[date]
        d["temps"].append(item["main"]["temp"])
        d["humidity"].append(item["main"]["humidity"])
        d["wind_speed"].append(item["wind"]["speed"])
        d["descriptions"].append(item["weather"][0]["description"])
        d["rain"] += item.get("rain", {}).get("3h", 0.0)
    result = []
    for i, (date, d) in enumerate(sorted(days.items())[:5], 1):
        result.append({
            "day": f"Day {i}", "date": date,
            "temp_max": round(max(d["temps"]),1),
            "temp_min": round(min(d["temps"]),1),
            "humidity": round(sum(d["humidity"])/len(d["humidity"]),1),
            "rain": round(d["rain"],1),
            "wind_speed": round(sum(d["wind_speed"])/len(d["wind_speed"]),1),
            "description": Counter(d["descriptions"]).most_common(1)[0][0],
        })
    return result
