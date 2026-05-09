"""
visualizer.py  –  Matplotlib charts for weather data
"""
import os
import matplotlib
matplotlib.use("Agg")          # headless – no display needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = {
    "bg":     "#0d1117",
    "card":   "#161b22",
    "accent": "#58a6ff",
    "warm":   "#ff7b72",
    "cool":   "#79c0ff",
    "green":  "#3fb950",
    "yellow": "#d29922",
    "text":   "#e6edf3",
    "muted":  "#8b949e",
}

def _setup_dark_fig(figsize=(12, 6), title=""):
    fig, ax = plt.subplots(figsize=figsize, facecolor=PALETTE["bg"])
    ax.set_facecolor(PALETTE["card"])
    ax.tick_params(colors=PALETTE["text"], labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(PALETTE["muted"])
    if title:
        ax.set_title(title, color=PALETTE["text"], fontsize=13, fontweight="bold", pad=12)
    return fig, ax

def save_temperature_chart(city: str, forecast: list) -> str:
    days       = [d["day"] for d in forecast]
    temp_max   = [d["temp_max"] for d in forecast]
    temp_min   = [d["temp_min"] for d in forecast]
    x          = np.arange(len(days))

    fig, ax = _setup_dark_fig(title=f"🌡  5-Day Temperature Forecast – {city}")
    ax.fill_between(x, temp_min, temp_max, alpha=0.25, color=PALETTE["accent"])
    ax.plot(x, temp_max, "o-", color=PALETTE["warm"],  lw=2.5, ms=7, label="Max Temp")
    ax.plot(x, temp_min, "o-", color=PALETTE["cool"],  lw=2.5, ms=7, label="Min Temp")

    for i, (mx, mn) in enumerate(zip(temp_max, temp_min)):
        ax.annotate(f"{mx}°", (i, mx), textcoords="offset points",
                    xytext=(0, 8), ha="center", color=PALETTE["warm"], fontsize=9)
        ax.annotate(f"{mn}°", (i, mn), textcoords="offset points",
                    xytext=(0, -14), ha="center", color=PALETTE["cool"], fontsize=9)

    ax.set_xticks(x); ax.set_xticklabels(days, color=PALETTE["text"])
    ax.set_ylabel("Temperature (°C)", color=PALETTE["text"])
    ax.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["muted"],
              labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.2, color=PALETTE["muted"])
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"{city.replace(' ','_')}_temperature.png")
    fig.savefig(path, dpi=130, facecolor=PALETTE["bg"])
    plt.close(fig)
    return path

def save_humidity_chart(city: str, forecast: list) -> str:
    days     = [d["day"] for d in forecast]
    humidity = [d["humidity"] for d in forecast]
    x        = np.arange(len(days))

    fig, ax = _setup_dark_fig(title=f"💧  5-Day Humidity Forecast – {city}")
    bars = ax.bar(x, humidity, color=PALETTE["accent"], alpha=0.8, width=0.55,
                  edgecolor=PALETTE["bg"])
    # Colour bars red when > 80
    for bar, h in zip(bars, humidity):
        if h > 80: bar.set_color(PALETTE["warm"])
    ax.axhline(80, color=PALETTE["yellow"], ls="--", lw=1.5, alpha=0.8, label="80% threshold")
    for bar, h in zip(bars, humidity):
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.0f}%",
                ha="center", va="bottom", color=PALETTE["text"], fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(days, color=PALETTE["text"])
    ax.set_ylabel("Humidity (%)", color=PALETTE["text"])
    ax.set_ylim(0, 110)
    ax.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["muted"],
              labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.2, color=PALETTE["muted"])
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"{city.replace(' ','_')}_humidity.png")
    fig.savefig(path, dpi=130, facecolor=PALETTE["bg"])
    plt.close(fig)
    return path

def save_rainfall_chart(city: str, forecast: list) -> str:
    days = [d["day"] for d in forecast]
    rain = [d.get("rain", 0) for d in forecast]
    x    = np.arange(len(days))

    fig, ax = _setup_dark_fig(title=f"🌧  5-Day Rainfall Forecast – {city}")
    colors = [PALETTE["warm"] if r >= 15 else PALETTE["cool"] if r >= 5 else PALETTE["green"]
              for r in rain]
    bars = ax.bar(x, rain, color=colors, alpha=0.85, width=0.55,
                  edgecolor=PALETTE["bg"])
    ax.axhline(15, color=PALETTE["yellow"], ls="--", lw=1.5, alpha=0.8, label="15 mm threshold")
    for bar, r in zip(bars, rain):
        if r > 0:
            ax.text(bar.get_x() + bar.get_width()/2, r + 0.3, f"{r} mm",
                    ha="center", va="bottom", color=PALETTE["text"], fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(days, color=PALETTE["text"])
    ax.set_ylabel("Rainfall (mm)", color=PALETTE["text"])
    legend_patches = [
        mpatches.Patch(color=PALETTE["green"], label="Light (<5mm)"),
        mpatches.Patch(color=PALETTE["cool"],  label="Moderate (5-15mm)"),
        mpatches.Patch(color=PALETTE["warm"],  label="Heavy (>15mm)"),
    ]
    ax.legend(handles=legend_patches, facecolor=PALETTE["card"],
              edgecolor=PALETTE["muted"], labelcolor=PALETTE["text"])
    ax.grid(axis="y", alpha=0.2, color=PALETTE["muted"])
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, f"{city.replace(' ','_')}_rainfall.png")
    fig.savefig(path, dpi=130, facecolor=PALETTE["bg"])
    plt.close(fig)
    return path

def save_dashboard_chart(city: str, current: dict, forecast: list) -> str:
    """4-panel summary dashboard."""
    fig = plt.figure(figsize=(14, 9), facecolor=PALETTE["bg"])
    fig.suptitle(f"🌤  Weather Dashboard – {city}  ({current['fetched_at']})",
                 color=PALETTE["text"], fontsize=14, fontweight="bold", y=0.97)

    days     = [d["day"] for d in forecast]
    temp_max = [d["temp_max"] for d in forecast]
    temp_min = [d["temp_min"] for d in forecast]
    humidity = [d["humidity"] for d in forecast]
    rain     = [d.get("rain", 0) for d in forecast]
    wind     = [d["wind_speed"] for d in forecast]
    x        = np.arange(len(days))

    def ax_style(ax, title):
        ax.set_facecolor(PALETTE["card"])
        ax.tick_params(colors=PALETTE["text"], labelsize=8)
        for sp in ax.spines.values(): sp.set_edgecolor(PALETTE["muted"])
        ax.set_title(title, color=PALETTE["text"], fontsize=10, fontweight="bold")
        ax.grid(axis="y", alpha=0.15, color=PALETTE["muted"])

    # Panel 1 – Temperature
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.fill_between(x, temp_min, temp_max, alpha=0.2, color=PALETTE["accent"])
    ax1.plot(x, temp_max, "o-", color=PALETTE["warm"], lw=2, ms=6, label="Max")
    ax1.plot(x, temp_min, "o-", color=PALETTE["cool"], lw=2, ms=6, label="Min")
    ax1.set_xticks(x); ax1.set_xticklabels(days)
    ax1.set_ylabel("°C", color=PALETTE["text"])
    ax1.legend(facecolor=PALETTE["card"], labelcolor=PALETTE["text"], fontsize=8)
    ax_style(ax1, "🌡  Temperature")

    # Panel 2 – Humidity
    ax2 = fig.add_subplot(2, 2, 2)
    bar_colors = [PALETTE["warm"] if h > 80 else PALETTE["accent"] for h in humidity]
    ax2.bar(x, humidity, color=bar_colors, alpha=0.8, width=0.5)
    ax2.axhline(80, color=PALETTE["yellow"], ls="--", lw=1.2)
    ax2.set_xticks(x); ax2.set_xticklabels(days)
    ax2.set_ylabel("%", color=PALETTE["text"])
    ax_style(ax2, "💧  Humidity")

    # Panel 3 – Rainfall
    ax3 = fig.add_subplot(2, 2, 3)
    rain_colors = [PALETTE["warm"] if r >= 15 else PALETTE["cool"] if r >= 5 else PALETTE["green"]
                   for r in rain]
    ax3.bar(x, rain, color=rain_colors, alpha=0.85, width=0.5)
    ax3.axhline(15, color=PALETTE["yellow"], ls="--", lw=1.2)
    ax3.set_xticks(x); ax3.set_xticklabels(days)
    ax3.set_ylabel("mm", color=PALETTE["text"])
    ax_style(ax3, "🌧  Rainfall")

    # Panel 4 – Wind
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.fill_between(x, 0, wind, alpha=0.3, color=PALETTE["green"])
    ax4.plot(x, wind, "o-", color=PALETTE["green"], lw=2, ms=6)
    ax4.axhline(20, color=PALETTE["warm"], ls="--", lw=1.2, label="Alert 20 m/s")
    ax4.set_xticks(x); ax4.set_xticklabels(days)
    ax4.set_ylabel("m/s", color=PALETTE["text"])
    ax4.legend(facecolor=PALETTE["card"], labelcolor=PALETTE["text"], fontsize=8)
    ax_style(ax4, "💨  Wind Speed")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(OUTPUT_DIR, f"{city.replace(' ','_')}_dashboard.png")
    fig.savefig(path, dpi=130, facecolor=PALETTE["bg"])
    plt.close(fig)
    return path
