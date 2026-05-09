"""
report_generator.py  –  Save weather data + alerts to CSV and TXT reports
"""
import os, csv
from datetime import datetime

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def _filename(city: str, ext: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city = city.replace(" ", "_")
    return os.path.join(REPORT_DIR, f"{safe_city}_report_{ts}.{ext}")

def save_csv_report(city: str, current: dict, forecast: list, alerts: list) -> str:
    """Save full weather report as CSV."""
    path = _filename(city, "csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["WEATHER FORECAST & ALERT REPORT"])
        writer.writerow(["City", city, "Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])

        # Current weather
        writer.writerow(["=== CURRENT WEATHER ==="])
        writer.writerow(["Metric", "Value"])
        for k, v in current.items():
            writer.writerow([k.replace("_", " ").title(), v])
        writer.writerow([])

        # Forecast table
        writer.writerow(["=== 5-DAY FORECAST ==="])
        writer.writerow(["Day", "Max Temp (°C)", "Min Temp (°C)",
                          "Humidity (%)", "Rain (mm)", "Wind (m/s)", "Description"])
        for d in forecast:
            writer.writerow([d["day"], d["temp_max"], d["temp_min"],
                              d["humidity"], d.get("rain", 0), d["wind_speed"], d["description"]])
        writer.writerow([])

        # Alerts
        writer.writerow(["=== WEATHER ALERTS ==="])
        writer.writerow(["Level", "Category", "Message", "Value", "Unit"])
        for alert in alerts:
            writer.writerow([alert.level, alert.category,
                              alert.message, alert.value, alert.unit])
    return path

def save_txt_report(city: str, current: dict, forecast: list, alerts: list) -> str:
    """Save a human-readable text report."""
    path = _filename(city, "txt")
    sep = "=" * 60
    with open(path, "w") as f:
        f.write(f"{sep}\n")
        f.write(f"  WEATHER FORECAST & ALERT REPORT\n")
        f.write(f"  City : {city}\n")
        f.write(f"  Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{sep}\n\n")

        f.write("CURRENT WEATHER\n" + "-"*40 + "\n")
        for k, v in current.items():
            f.write(f"  {k.replace('_',' ').title():<20}: {v}\n")

        f.write(f"\n5-DAY FORECAST\n" + "-"*40 + "\n")
        f.write(f"{'Day':<8} {'MaxC':>6} {'MinC':>6} {'Hum%':>6} "
                f"{'Rain':>8} {'Wind':>8}  Description\n")
        for d in forecast:
            f.write(f"{d['day']:<8} {d['temp_max']:>6.1f} {d['temp_min']:>6.1f} "
                    f"{d['humidity']:>6.0f} {d.get('rain',0):>8.1f} "
                    f"{d['wind_speed']:>8.1f}  {d['description'].title()}\n")

        f.write(f"\nWEATHER ALERTS\n" + "-"*40 + "\n")
        for alert in alerts:
            # Strip ANSI codes for the text file
            f.write(f"  [{alert.level}] {alert.category}: {alert.message}\n")

        f.write(f"\n{sep}\n")
    return path
