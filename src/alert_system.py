"""
alert_system.py  –  Weather alert logic
Checks conditions and returns colour-coded alert messages.
"""
from dataclasses import dataclass, field

# ── Default thresholds ─────────────────────────────────────────────────────────
THRESHOLDS = {
    "temp_high":     40.0,   # °C
    "temp_low":       5.0,   # °C
    "humidity_high": 85.0,   # %
    "wind_high":     20.0,   # m/s
    "rain_high":     15.0,   # mm
    "uvi_high":       8.0,   # UV index
}

# ANSI colours for terminal output
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

@dataclass
class Alert:
    level:    str   # "CRITICAL" | "WARNING" | "INFO"
    category: str
    message:  str
    value:    float
    unit:     str

    @property
    def colour(self):
        return {
            "CRITICAL": RED,
            "WARNING":  YELLOW,
            "INFO":     CYAN,
        }.get(self.level, RESET)

    def __str__(self):
        icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}.get(self.level, "⚪")
        return (f"{self.colour}{BOLD}{icon} [{self.level}] {self.category}: "
                f"{self.message} ({self.value}{self.unit}){RESET}")


def check_alerts(current: dict, forecast: list, thresholds: dict = None) -> list:
    """
    Analyse current weather + forecast and return a list of Alert objects.
    """
    t = {**THRESHOLDS, **(thresholds or {})}
    alerts = []

    # ── Current conditions ────────────────────────────────────────────────────
    temp = current.get("temp", 0)
    if temp >= t["temp_high"] + 5:
        alerts.append(Alert("CRITICAL", "Extreme Heat",
                            f"Temperature is dangerously high at {temp}°C!",
                            temp, "°C"))
    elif temp >= t["temp_high"]:
        alerts.append(Alert("WARNING", "High Temperature",
                            f"Temperature exceeds threshold ({t['temp_high']}°C)",
                            temp, "°C"))

    if temp <= t["temp_low"]:
        alerts.append(Alert("WARNING", "Low Temperature",
                            f"Temperature below {t['temp_low']}°C – risk of frost",
                            temp, "°C"))

    humidity = current.get("humidity", 0)
    if humidity >= t["humidity_high"]:
        alerts.append(Alert("WARNING", "High Humidity",
                            f"Humidity at {humidity}% – discomfort risk",
                            humidity, "%"))

    wind = current.get("wind_speed", 0)
    if wind >= t["wind_high"] + 10:
        alerts.append(Alert("CRITICAL", "Storm Warning",
                            f"Wind speed {wind} m/s – dangerous conditions!",
                            wind, " m/s"))
    elif wind >= t["wind_high"]:
        alerts.append(Alert("WARNING", "Strong Winds",
                            f"Wind speed {wind} m/s exceeds safe threshold",
                            wind, " m/s"))

    desc = current.get("description", "").lower()
    if any(w in desc for w in ["thunderstorm", "tornado", "hurricane"]):
        alerts.append(Alert("CRITICAL", "Severe Weather",
                            f"Severe weather detected: {desc.title()}!",
                            0, ""))
    elif any(w in desc for w in ["heavy rain", "heavy intensity rain"]):
        alerts.append(Alert("WARNING", "Heavy Rain",
                            f"Heavy rainfall reported: {desc.title()}",
                            0, ""))

    # ── Forecast alerts ───────────────────────────────────────────────────────
    for day in forecast:
        if day.get("rain", 0) >= t["rain_high"]:
            alerts.append(Alert("WARNING", f"Rain Forecast ({day['day']})",
                                f"Expected {day['rain']} mm rainfall",
                                day["rain"], " mm"))
        if day.get("temp_max", 0) >= t["temp_high"]:
            alerts.append(Alert("INFO", f"Heat Forecast ({day['day']})",
                                f"Max temp {day['temp_max']}°C expected",
                                day["temp_max"], "°C"))
        if day.get("wind_speed", 0) >= t["wind_high"]:
            alerts.append(Alert("INFO", f"Wind Forecast ({day['day']})",
                                f"Wind {day['wind_speed']} m/s expected",
                                day["wind_speed"], " m/s"))

    if not alerts:
        alerts.append(Alert("INFO", "All Clear",
                            "No severe weather alerts at this time ✅",
                            0, ""))
    return alerts


def get_overall_severity(alerts: list) -> str:
    """Return highest severity level found in alerts list."""
    levels = [a.level for a in alerts]
    if "CRITICAL" in levels: return "CRITICAL"
    if "WARNING"  in levels: return "WARNING"
    return "INFO"
