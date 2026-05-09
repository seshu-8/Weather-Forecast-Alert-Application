"""
data_parser.py  –  Format and display weather data in the terminal
"""

BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BLUE   = "\033[94m"

def wind_direction(deg: float) -> str:
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[round(deg / 45) % 8]

def display_current(data: dict):
    """Pretty-print current weather to terminal."""
    mode_tag = f" [{data.get('mode','LIVE')}]" if data.get('mode') else ""
    print(f"\n{BOLD}{CYAN}{'═'*55}{RESET}")
    print(f"{BOLD}{CYAN}  🌤  CURRENT WEATHER – {data['city']}, {data['country']}{mode_tag}{RESET}")
    print(f"{BOLD}{CYAN}{'═'*55}{RESET}")
    print(f"  📅  Fetched at   : {data['fetched_at']}")
    print(f"  🌡  Temperature  : {data['temp']}°C  (feels like {data['feels_like']}°C)")
    print(f"  🔼  High / Low   : {data['temp_max']}°C / {data['temp_min']}°C")
    print(f"  💧  Humidity     : {data['humidity']}%")
    print(f"  🔵  Pressure     : {data['pressure']} hPa")
    print(f"  💨  Wind         : {data['wind_speed']} m/s  {wind_direction(data['wind_deg'])}")
    print(f"  👁  Visibility   : {data['visibility']/1000:.1f} km")
    print(f"  🌅  Sunrise      : {data['sunrise']}    🌇 Sunset: {data['sunset']}")
    print(f"  ☁  Condition    : {data['description'].title()}")
    print(f"{CYAN}{'─'*55}{RESET}")

def display_forecast(forecast: list):
    """Pretty-print 5-day forecast table."""
    print(f"\n{BOLD}{BLUE}{'═'*65}{RESET}")
    print(f"{BOLD}{BLUE}  📅  5-DAY FORECAST{RESET}")
    print(f"{BOLD}{BLUE}{'═'*65}{RESET}")
    header = f"{'Day':<8} {'Max°C':>6} {'Min°C':>6} {'Hum%':>6} {'Rain mm':>8} {'Wind m/s':>9}  Description"
    print(f"{BOLD}{header}{RESET}")
    print(f"{'─'*65}")
    for d in forecast:
        rain_str = f"{d.get('rain',0):>8.1f}" if d.get('rain',0) else "       –"
        print(f"{d['day']:<8} {d['temp_max']:>6.1f} {d['temp_min']:>6.1f} "
              f"{d['humidity']:>6.0f} {rain_str} {d['wind_speed']:>9.1f}  {d['description'].title()}")
    print(f"{BLUE}{'─'*65}{RESET}")

def display_alerts(alerts: list):
    """Print alert section."""
    print(f"\n{BOLD}{'═'*55}{RESET}")
    print(f"{BOLD}  🚨  WEATHER ALERTS{RESET}")
    print(f"{'═'*55}")
    for alert in alerts:
        print(f"  {alert}")
    print(f"{'─'*55}")
