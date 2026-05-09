"""
dashboard.py  –  Streamlit Interactive Dashboard
=================================================
Run with:  streamlit run dashboard.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

from simulation   import fetch_simulated_current, fetch_simulated_forecast, get_available_cities
from alert_system import check_alerts, get_overall_severity

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weather Forecast & Alert App",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
}

/* Metric cards */
.weather-metric {
    background: linear-gradient(135deg, #161b22, #21262d);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.2s;
}
.weather-metric:hover { transform: translateY(-2px); }
.metric-icon  { font-size: 2rem; margin-bottom: 4px; }
.metric-label { color: #8b949e; font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; }
.metric-value { color: #e6edf3; font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.metric-sub   { color: #58a6ff; font-size: 0.78rem; margin-top: 2px; }

/* Alert badges */
.alert-critical { background:#2d1a1a; border-left:4px solid #f85149; padding:10px 16px; border-radius:8px; margin:6px 0; }
.alert-warning  { background:#2d2600; border-left:4px solid #d29922; padding:10px 16px; border-radius:8px; margin:6px 0; }
.alert-info     { background:#0d1d2e; border-left:4px solid #58a6ff; padding:10px 16px; border-radius:8px; margin:6px 0; }
.alert-text     { color:#e6edf3; font-size:0.9rem; }

/* City badge */
.city-badge {
    background: linear-gradient(90deg, #58a6ff22, #79c0ff11);
    border: 1px solid #58a6ff44;
    border-radius: 999px;
    padding: 6px 20px;
    display: inline-block;
    color: #58a6ff;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Section headers */
.section-header {
    color: #8b949e;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 24px 0 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #21262d;
}

/* Severity banner */
.sev-critical { background:#2d1a1a; border:1px solid #f85149; border-radius:10px; padding:12px 20px; text-align:center; }
.sev-warning  { background:#2d2600; border:1px solid #d29922; border-radius:10px; padding:12px 20px; text-align:center; }
.sev-info     { background:#0d1d2e; border:1px solid #58a6ff; border-radius:10px; padding:12px 20px; text-align:center; }
.sev-text     { color:#e6edf3; font-size:1.05rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ── Colour palette ─────────────────────────────────────────────────────────────
PAL = {
    "bg": "#0d1117", "card": "#161b22", "accent": "#58a6ff",
    "warm": "#ff7b72", "cool": "#79c0ff", "green": "#3fb950",
    "yellow": "#d29922", "text": "#e6edf3", "muted": "#8b949e",
}

def ax_dark(ax, title=""):
    ax.set_facecolor(PAL["card"])
    ax.tick_params(colors=PAL["text"], labelsize=9)
    for sp in ax.spines.values(): sp.set_edgecolor(PAL["muted"])
    if title: ax.set_title(title, color=PAL["text"], fontsize=11, fontweight="bold", pad=10)
    ax.grid(axis="y", alpha=0.15, color=PAL["muted"])

# ── Helper: wind direction ─────────────────────────────────────────────────────
def wind_dir(deg):
    return ["N","NE","E","SE","S","SW","W","NW"][round(deg/45)%8]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌤 Weather App")
    st.markdown("---")

    mode = st.radio("Data Source", ["🎮 Simulation (Offline)", "🌐 Live API"],
                    index=0, help="Simulation uses built-in sample data. API requires OpenWeatherMap key.")
    live = "API" in mode

    api_key = None
    if live:
        st.markdown(
            "<small>🔑 Get a free key at "
            "<a href='https://openweathermap.org/api' target='_blank'>openweathermap.org</a>"
            "<br>⚠️ <b>New keys take up to 2 hours to activate.</b></small>",
            unsafe_allow_html=True
        )
        api_key_raw = st.text_input(
            "OpenWeatherMap API Key",
            type="password",
            placeholder="Paste your 32-char key here",
            help="Copy from openweathermap.org My API Keys page"
        )
        # Strip ALL whitespace/newlines — common copy-paste issue causing 401
        api_key = api_key_raw.strip() if api_key_raw else None

        if api_key:
            char_count = len(api_key)
            if char_count != 32:
                st.warning(f"Key is {char_count} chars — valid OWM keys are exactly 32 characters. Check for extra spaces.")
            else:
                st.success(f"Key format OK ({char_count}/32 chars)")

            if st.button("🧪 Test API Key", use_container_width=True):
                from weather_api import validate_api_key
                with st.spinner("Testing key against OpenWeatherMap..."):
                    result = validate_api_key(api_key)
                if result["valid"]:
                    st.success(result["message"])
                else:
                    for line in result["message"].split("\n"):
                        st.error(line) if line.startswith("❌") else st.warning(line)

        city = st.text_input("City Name", placeholder="e.g. Mumbai, London, Tokyo")
    else:
        city = st.selectbox("Select City", get_available_cities())

    st.markdown("---")
    st.markdown("### ⚙️ Alert Thresholds")
    th_temp   = st.slider("High Temp (°C)",     30, 50, 40)
    th_hum    = st.slider("High Humidity (%)",   60, 100, 85)
    th_wind   = st.slider("High Wind (m/s)",     10, 40, 20)
    th_rain   = st.slider("High Rain (mm)",       5, 50, 15)
    thresholds = {"temp_high": th_temp, "humidity_high": th_hum,
                  "wind_high": th_wind, "rain_high": th_rain}

    run_btn = st.button("🔍 Get Weather", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("Built with Python · Streamlit · Matplotlib")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
if not run_btn and "weather_data" not in st.session_state:
    # Landing screen
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px;'>
      <div style='font-size:5rem;'>🌤⛈🌡</div>
      <h1 style='color:#e6edf3; font-size:2.6rem; font-weight:700; margin:20px 0 10px;'>
        Weather Forecast &amp; Alert Application
      </h1>
      <p style='color:#8b949e; font-size:1.1rem; max-width:600px; margin:0 auto 32px;'>
        A full-stack weather dashboard for students — featuring live API integration,
        offline simulation, smart alerts, and beautiful visualisations.
      </p>
      <div style='display:flex; gap:16px; justify-content:center; flex-wrap:wrap;'>
        <span style='background:#21262d; border:1px solid #30363d; border-radius:999px; padding:8px 20px; color:#58a6ff; font-size:0.85rem;'>🐍 Python</span>
        <span style='background:#21262d; border:1px solid #30363d; border-radius:999px; padding:8px 20px; color:#3fb950; font-size:0.85rem;'>📡 OpenWeatherMap API</span>
        <span style='background:#21262d; border:1px solid #30363d; border-radius:999px; padding:8px 20px; color:#d29922; font-size:0.85rem;'>📊 Matplotlib</span>
        <span style='background:#21262d; border:1px solid #30363d; border-radius:999px; padding:8px 20px; color:#ff7b72; font-size:0.85rem;'>🚨 Smart Alerts</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("👈  Select a city from the sidebar and click **Get Weather** to begin.")
    st.stop()

# ── Fetch / cache data ─────────────────────────────────────────────────────────
if run_btn:
    if live and not api_key:
        st.error("❌  Please paste your OpenWeatherMap API key in the sidebar first.")
        st.stop()
    if live and not city:
        st.error("❌  Please enter a city name.")
        st.stop()
    with st.spinner("Fetching weather data …"):
        try:
            if live:
                from weather_api import fetch_current_weather, fetch_forecast
                # Pass api_key directly (already stripped in sidebar)
                current  = fetch_current_weather(city, api_key=api_key)
                forecast = fetch_forecast(city, api_key=api_key)
            else:
                current  = fetch_simulated_current(city)
                forecast = fetch_simulated_forecast(city)
            st.session_state["weather_data"] = (city, current, forecast, thresholds)
        except PermissionError as e:
            st.error(f"🔑 API Key Error")
            for line in str(e).split("\n"):
                st.warning(line) if line.strip() else None
            st.info("💡 While waiting for key activation, switch to **Simulation Mode** to explore all features offline.")
            st.stop()
        except Exception as e:
            st.error(f"❌  {e}")
            st.stop()

city, current, forecast, thresholds = st.session_state["weather_data"]
alerts   = check_alerts(current, forecast, thresholds)
severity = get_overall_severity(alerts)

# ── City header ────────────────────────────────────────────────────────────────
mode_tag = "🎮 SIMULATION" if current.get("mode") else "🌐 LIVE"
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"# 🌤 {city}", unsafe_allow_html=True)
    st.markdown(f"<span class='city-badge'>{mode_tag} · {current['fetched_at']}</span>",
                unsafe_allow_html=True)
with col_h2:
    sev_cls = {"CRITICAL":"sev-critical","WARNING":"sev-warning","INFO":"sev-info"}[severity]
    sev_icon = {"CRITICAL":"🔴","WARNING":"🟡","INFO":"🟢"}[severity]
    st.markdown(f"<div class='{sev_cls}'><div class='sev-text'>{sev_icon} {severity}</div><div style='color:#8b949e;font-size:0.75rem;'>{len(alerts)} alert(s)</div></div>",
                unsafe_allow_html=True)

st.markdown("---")

# ── Current weather metrics ────────────────────────────────────────────────────
st.markdown("<div class='section-header'>Current Conditions</div>", unsafe_allow_html=True)
m1, m2, m3, m4, m5, m6 = st.columns(6)

def metric_card(icon, label, value, sub=""):
    return f"""<div class='weather-metric'>
      <div class='metric-icon'>{icon}</div>
      <div class='metric-label'>{label}</div>
      <div class='metric-value'>{value}</div>
      {"<div class='metric-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

with m1: st.markdown(metric_card("🌡", "Temperature", f"{current['temp']}°C", f"Feels {current['feels_like']}°C"), unsafe_allow_html=True)
with m2: st.markdown(metric_card("💧", "Humidity", f"{current['humidity']}%", "Relative humidity"), unsafe_allow_html=True)
with m3: st.markdown(metric_card("💨", "Wind", f"{current['wind_speed']} m/s", wind_dir(current['wind_deg'])), unsafe_allow_html=True)
with m4: st.markdown(metric_card("🔵", "Pressure", f"{current['pressure']} hPa", "Atmospheric"), unsafe_allow_html=True)
with m5: st.markdown(metric_card("👁", "Visibility", f"{current['visibility']/1000:.1f} km", "Clear/Hazy"), unsafe_allow_html=True)
with m6: st.markdown(metric_card("☁", "Condition", current['description'].split()[-1].title(), current['description'].title()), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "📅 Forecast Table", "🚨 Alerts", "📄 Report"])

days       = [d["day"] for d in forecast]
temp_max   = [d["temp_max"] for d in forecast]
temp_min   = [d["temp_min"] for d in forecast]
humidity   = [d["humidity"] for d in forecast]
rain       = [d.get("rain", 0) for d in forecast]
wind_vals  = [d["wind_speed"] for d in forecast]
x          = np.arange(len(days))

# ── Tab 1: Charts ──────────────────────────────────────────────────────────────
with tab1:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Temperature chart
        fig, ax = plt.subplots(figsize=(7, 4), facecolor=PAL["bg"])
        ax.fill_between(x, temp_min, temp_max, alpha=0.22, color=PAL["accent"])
        ax.plot(x, temp_max, "o-", color=PAL["warm"], lw=2.5, ms=7, label="Max °C")
        ax.plot(x, temp_min, "o-", color=PAL["cool"], lw=2.5, ms=7, label="Min °C")
        for i, (mx, mn) in enumerate(zip(temp_max, temp_min)):
            ax.annotate(f"{mx}°", (i, mx), xytext=(0,8), textcoords="offset points",
                        ha="center", color=PAL["warm"], fontsize=9)
            ax.annotate(f"{mn}°", (i, mn), xytext=(0,-14), textcoords="offset points",
                        ha="center", color=PAL["cool"], fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(days)
        ax.set_ylabel("°C", color=PAL["text"])
        ax.legend(facecolor=PAL["card"], labelcolor=PAL["text"])
        ax_dark(ax, "🌡  Temperature Forecast")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Rainfall chart
        fig, ax = plt.subplots(figsize=(7, 4), facecolor=PAL["bg"])
        rain_colors = [PAL["warm"] if r>=15 else PAL["cool"] if r>=5 else PAL["green"] for r in rain]
        ax.bar(x, rain, color=rain_colors, alpha=0.85, width=0.5, edgecolor=PAL["bg"])
        ax.axhline(thresholds.get("rain_high",15), color=PAL["yellow"], ls="--", lw=1.5, label="Alert")
        for i, r in enumerate(rain):
            if r > 0: ax.text(i, r+0.3, f"{r}mm", ha="center", color=PAL["text"], fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(days)
        ax.set_ylabel("mm", color=PAL["text"])
        legend_patches = [
            mpatches.Patch(color=PAL["green"], label="Light"),
            mpatches.Patch(color=PAL["cool"],  label="Moderate"),
            mpatches.Patch(color=PAL["warm"],  label="Heavy"),
        ]
        ax.legend(handles=legend_patches, facecolor=PAL["card"], labelcolor=PAL["text"])
        ax_dark(ax, "🌧  Rainfall Forecast")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with chart_col2:
        # Humidity chart
        fig, ax = plt.subplots(figsize=(7, 4), facecolor=PAL["bg"])
        hum_colors = [PAL["warm"] if h>thresholds.get("humidity_high",85) else PAL["accent"] for h in humidity]
        ax.bar(x, humidity, color=hum_colors, alpha=0.8, width=0.5, edgecolor=PAL["bg"])
        ax.axhline(thresholds.get("humidity_high",85), color=PAL["yellow"], ls="--", lw=1.5, label="Threshold")
        for i, h in enumerate(humidity):
            ax.text(i, h+1.5, f"{h:.0f}%", ha="center", color=PAL["text"], fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(days)
        ax.set_ylabel("%", color=PAL["text"])
        ax.set_ylim(0, 115)
        ax.legend(facecolor=PAL["card"], labelcolor=PAL["text"])
        ax_dark(ax, "💧  Humidity Forecast")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Wind chart
        fig, ax = plt.subplots(figsize=(7, 4), facecolor=PAL["bg"])
        ax.fill_between(x, 0, wind_vals, alpha=0.25, color=PAL["green"])
        ax.plot(x, wind_vals, "o-", color=PAL["green"], lw=2.5, ms=7, label="Wind m/s")
        ax.axhline(thresholds.get("wind_high",20), color=PAL["warm"], ls="--", lw=1.5, label="Alert")
        for i, w in enumerate(wind_vals):
            ax.annotate(f"{w}", (i, w), xytext=(0,8), textcoords="offset points",
                        ha="center", color=PAL["green"], fontsize=9)
        ax.set_xticks(x); ax.set_xticklabels(days)
        ax.set_ylabel("m/s", color=PAL["text"])
        ax.legend(facecolor=PAL["card"], labelcolor=PAL["text"])
        ax_dark(ax, "💨  Wind Speed Forecast")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# ── Tab 2: Forecast Table ──────────────────────────────────────────────────────
with tab2:
    df = pd.DataFrame(forecast)
    df_display = df[["day","temp_max","temp_min","humidity","rain","wind_speed","description"]].copy()
    df_display.columns = ["Day","Max °C","Min °C","Humidity %","Rain mm","Wind m/s","Condition"]
    df_display["Condition"] = df_display["Condition"].str.title()
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Highlight chart
    fig, ax = plt.subplots(figsize=(12, 3), facecolor=PAL["bg"])
    width = 0.35
    ax.bar(x - width/2, temp_max, width, label="Max °C", color=PAL["warm"], alpha=0.85)
    ax.bar(x + width/2, temp_min, width, label="Min °C", color=PAL["cool"], alpha=0.85)
    ax.set_xticks(x); ax.set_xticklabels(days)
    ax.set_ylabel("°C", color=PAL["text"])
    ax.legend(facecolor=PAL["card"], labelcolor=PAL["text"])
    ax_dark(ax, "Temperature Comparison (Max vs Min)")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ── Tab 3: Alerts ──────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"### {len(alerts)} Alert(s) Generated")
    for alert in alerts:
        css_cls = {
            "CRITICAL": "alert-critical",
            "WARNING":  "alert-warning",
            "INFO":     "alert-info",
        }.get(alert.level, "alert-info")
        icon = {"CRITICAL":"🔴","WARNING":"🟡","INFO":"🔵"}.get(alert.level,"⚪")
        st.markdown(
            f"<div class='{css_cls}'>"
            f"<span class='alert-text'>{icon} <strong>[{alert.level}]</strong> "
            f"<strong>{alert.category}</strong>: {alert.message}"
            f"{'  · '+str(alert.value)+alert.unit if alert.value else ''}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Alert distribution pie chart
    from collections import Counter
    lvl_counts = Counter(a.level for a in alerts)
    if len(lvl_counts) > 1:
        fig, ax = plt.subplots(figsize=(5, 3), facecolor=PAL["bg"])
        ax.set_facecolor(PAL["bg"])
        colors_map = {"CRITICAL": PAL["warm"], "WARNING": PAL["yellow"], "INFO": PAL["accent"]}
        colors_pie = [colors_map.get(k, PAL["muted"]) for k in lvl_counts.keys()]
        wedges, texts, autotexts = ax.pie(
            lvl_counts.values(), labels=lvl_counts.keys(),
            autopct="%1.0f%%", colors=colors_pie, startangle=90,
            textprops={"color": PAL["text"]})
        for at in autotexts: at.set_color(PAL["bg"]); at.set_fontweight("bold")
        ax.set_title("Alert Distribution", color=PAL["text"], fontweight="bold")
        fig.tight_layout()
        c1, c2, c3 = st.columns([1,2,1])
        with c2: st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# ── Tab 4: Report ──────────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 📄 Export Report")
    report_lines = []
    report_lines.append(f"WEATHER FORECAST & ALERT REPORT")
    report_lines.append(f"City: {city} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append("=" * 60)
    report_lines.append("\nCURRENT WEATHER")
    for k, v in current.items():
        report_lines.append(f"  {k.replace('_',' ').title():<20}: {v}")
    report_lines.append("\n5-DAY FORECAST")
    report_lines.append(f"{'Day':<8} {'Max':>5} {'Min':>5} {'Hum':>5} {'Rain':>7} {'Wind':>7}  Condition")
    report_lines.append("-" * 60)
    for d in forecast:
        report_lines.append(f"{d['day']:<8} {d['temp_max']:>5.1f} {d['temp_min']:>5.1f} "
                             f"{d['humidity']:>5.0f} {d.get('rain',0):>7.1f} "
                             f"{d['wind_speed']:>7.1f}  {d['description'].title()}")
    report_lines.append("\nWEATHER ALERTS")
    for alert in alerts:
        report_lines.append(f"  [{alert.level}] {alert.category}: {alert.message}")
    report_text = "\n".join(report_lines)

    st.text_area("Report Preview", report_text, height=350)
    st.download_button(
        label="⬇ Download TXT Report",
        data=report_text,
        file_name=f"{city.replace(' ','_')}_weather_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # CSV download
    df_csv = pd.DataFrame(forecast)
    csv_data = df_csv.to_csv(index=False)
    st.download_button(
        label="⬇ Download Forecast CSV",
        data=csv_data,
        file_name=f"{city.replace(' ','_')}_forecast.csv",
        mime="text/csv",
        use_container_width=True,
    )
