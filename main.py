#!/usr/bin/env python3
"""
main.py – Weather Forecast & Alert Application
================================================
Entry point. Supports two modes:
  --mode api  : Fetch live data from OpenWeatherMap (requires API key in .env)
  --mode sim  : Use offline simulation data (no API key needed)

Usage:
  python main.py                          # interactive prompt
  python main.py --city Mumbai            # auto city, sim mode default
  python main.py --city Delhi --mode api  # live API mode
  python main.py --city London --mode sim --no-charts  # skip charts
"""

import sys, os, argparse

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed; env vars from shell will still work

# Ensure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_parser       import display_current, display_forecast, display_alerts
from alert_system      import check_alerts, get_overall_severity
from report_generator  import save_csv_report, save_txt_report
from simulation        import fetch_simulated_current, fetch_simulated_forecast, get_available_cities

BOLD   = "\033[1m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
  ██     ██ ███████  █████  ████████ ██   ██ ███████ ██████
  ██     ██ ██      ██   ██    ██    ██   ██ ██      ██   ██
  ██  █  ██ █████   ███████    ██    ███████ █████   ██████
  ██ ███ ██ ██      ██   ██    ██    ██   ██ ██      ██   ██
   ███ ███  ███████ ██   ██    ██    ██   ██ ███████ ██   ██

        🌤  FORECAST & ALERT APPLICATION  ⛈
{RESET}"""

def parse_args():
    parser = argparse.ArgumentParser(
        description="Weather Forecast & Alert Application")
    parser.add_argument("--city",      default=None,  help="City name")
    parser.add_argument("--mode",      default="sim", choices=["api", "sim"],
                        help="'api' for live data, 'sim' for simulation (default: sim)")
    parser.add_argument("--no-charts", action="store_true",
                        help="Skip chart generation")
    parser.add_argument("--no-report", action="store_true",
                        help="Skip report generation")
    return parser.parse_args()


def get_city(args) -> str:
    if args.city:
        return args.city
    print(f"\n{BOLD}Available cities for simulation:{RESET}")
    for c in get_available_cities():
        print(f"  • {c}")
    city = input(f"\n{BOLD}Enter city name: {RESET}").strip()
    return city or "Mumbai"


def run(city: str, mode: str, charts: bool, report: bool):
    print(BANNER)
    print(f"{BOLD}  Mode : {GREEN if mode=='api' else YELLOW}{mode.upper()}{RESET}")
    print(f"  City : {city}\n")

    # ── Fetch data ─────────────────────────────────────────────────────────────
    if mode == "api":
        from weather_api import fetch_current_weather, fetch_forecast
        print("⏳  Fetching live weather data …")
        try:
            current  = fetch_current_weather(city)
            forecast = fetch_forecast(city)
        except Exception as e:
            print(f"\n{RED}❌  API Error: {e}{RESET}")
            print(f"{YELLOW}💡  Tip: Run with --mode sim to use offline simulation{RESET}\n")
            sys.exit(1)
    else:
        print("🎮  Loading simulation data …")
        try:
            current  = fetch_simulated_current(city)
            forecast = fetch_simulated_forecast(city)
        except ValueError as e:
            print(f"\n{RED}❌  {e}{RESET}\n")
            sys.exit(1)

    # ── Display ────────────────────────────────────────────────────────────────
    display_current(current)
    display_forecast(forecast)

    # ── Alerts ─────────────────────────────────────────────────────────────────
    alerts   = check_alerts(current, forecast)
    severity = get_overall_severity(alerts)
    display_alerts(alerts)

    sev_color = RED if severity == "CRITICAL" else YELLOW if severity == "WARNING" else GREEN
    print(f"\n  Overall Severity: {sev_color}{BOLD}{severity}{RESET}\n")

    # ── Visualizations ─────────────────────────────────────────────────────────
    if charts:
        try:
            import matplotlib
            from visualizer import (save_temperature_chart, save_humidity_chart,
                                    save_rainfall_chart, save_dashboard_chart)
            print("📊  Generating charts …")
            p1 = save_temperature_chart(city, forecast)
            p2 = save_humidity_chart(city, forecast)
            p3 = save_rainfall_chart(city, forecast)
            p4 = save_dashboard_chart(city, current, forecast)
            print(f"  {GREEN}✔{RESET} Temperature chart  → {p1}")
            print(f"  {GREEN}✔{RESET} Humidity chart     → {p2}")
            print(f"  {GREEN}✔{RESET} Rainfall chart     → {p3}")
            print(f"  {GREEN}✔{RESET} Dashboard chart    → {p4}")
        except ImportError:
            print(f"  {YELLOW}⚠  matplotlib not installed – skipping charts{RESET}")
        except Exception as e:
            print(f"  {YELLOW}⚠  Chart error: {e}{RESET}")

    # ── Reports ────────────────────────────────────────────────────────────────
    if report:
        print("\n📄  Generating reports …")
        csv_path = save_csv_report(city, current, forecast, alerts)
        txt_path = save_txt_report(city, current, forecast, alerts)
        print(f"  {GREEN}✔{RESET} CSV report → {csv_path}")
        print(f"  {GREEN}✔{RESET} TXT report → {txt_path}")

    print(f"\n{CYAN}{'═'*55}{RESET}")
    print(f"  ✅  Analysis complete for {BOLD}{city}{RESET}")
    print(f"{CYAN}{'═'*55}{RESET}\n")


def main():
    args   = parse_args()
    city   = get_city(args)
    charts = not args.no_charts
    report = not args.no_report
    run(city, args.mode, charts, report)


if __name__ == "__main__":
    main()
