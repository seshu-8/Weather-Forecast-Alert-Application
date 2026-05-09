<div align="center">

# 🌤 Weather Forecast & Alert Application

**A production-grade Python project for fetching, analysing, and visualising weather data with smart alert generation.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-orange?logo=data:image/png;base64,)](https://openweathermap.org/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## 📖 Project Overview

This project is a **full-featured weather forecasting and alert application** built in Python. It fetches live weather data from the **OpenWeatherMap API** (or uses built-in simulation data offline), analyses it, generates smart alerts, creates beautiful visualisations, and saves reports — all from the command line **and** a rich Streamlit web dashboard.

---

## 🎯 Problem Statement

- Weather affects **everyone**: travellers, farmers, logistics companies, event planners, and daily commuters.
- Manual weather checking is inefficient at scale.
- Automated alert systems save lives and reduce losses.
- This project demonstrates API integration, data analysis, alerting logic, and dashboard development — all in-demand industry skills.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌐 Live API Mode | Fetches real-time weather from OpenWeatherMap |
| 🎮 Simulation Mode | Works fully offline using sample data |
| 📅 5-Day Forecast | Daily summaries with temp, humidity, rain, wind |
| 🚨 Smart Alerts | CRITICAL / WARNING / INFO with custom thresholds |
| 📊 4 Charts | Temperature, humidity, rainfall, wind speed |
| 🖥 Dashboard | Interactive Streamlit web app |
| 📄 CSV + TXT Reports | Auto-saved in `reports/` folder |
| 🛡 Secure | API key via `.env` file, never in code |

---

## 🛠 Tech Stack

```
Python 3.10+       →  Core language
requests           →  HTTP API calls
python-dotenv      →  Secure API key management
pandas             →  Data manipulation & CSV
matplotlib         →  Chart generation
numpy              →  Numerical operations
streamlit          →  Interactive web dashboard
json / datetime    →  Built-in data handling
```

---

## 📁 Folder Structure

```
Weather-Forecast-Alert-Application/
│
├── data/
│   └── sample_weather.json     ← Offline simulation data (5 cities)
│
├── src/
│   ├── weather_api.py          ← Live OpenWeatherMap API calls
│   ├── simulation.py           ← Offline simulation logic
│   ├── alert_system.py         ← Alert generation (CRITICAL/WARNING/INFO)
│   ├── data_parser.py          ← Terminal display formatting
│   ├── visualizer.py           ← Matplotlib chart generation
│   └── report_generator.py     ← CSV + TXT report saving
│
├── outputs/                    ← Generated chart images (PNG)
├── reports/                    ← Generated CSV + TXT reports
├── images/                     ← Screenshots for GitHub README
├── docs/                       ← Additional documentation
│
├── main.py                     ← CLI entry point
├── dashboard.py                ← Streamlit web dashboard
├── requirements.txt            ← All Python dependencies
├── .env.example                ← API key template (safe to commit)
├── .gitignore                  ← Excludes .env, outputs, __pycache__
└── README.md                   ← This file
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Weather-Forecast-Alert-Application.git
cd Weather-Forecast-Alert-Application
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key (Optional – for live mode)
```bash
cp .env.example .env
# Edit .env and paste your OpenWeatherMap API key
# Get a free key at: https://openweathermap.org/api
```

---

## 🚀 How to Run

### CLI – Simulation Mode (No API key needed)
```bash
python main.py --city Mumbai --mode sim
python main.py --city Delhi
python main.py --city London --mode sim --no-charts
```

### CLI – Live API Mode
```bash
python main.py --city Paris --mode api
python main.py --city Tokyo --mode api --no-report
```

### Interactive (prompts for city)
```bash
python main.py
```

### Streamlit Dashboard
```bash
streamlit run dashboard.py
# Opens at http://localhost:8501
```

---

## 🌆 Sample Cities (Simulation Mode)

| City | Scenario |
|---|---|
| Mumbai | Heavy rain + high humidity alerts |
| Delhi | Extreme heat (45°C) critical alert |
| Bengaluru | Pleasant weather, no alerts |
| London | High winds + rain forecast |
| New York | Mixed forecast, moderate rain |

---

## 📊 Sample Output

```
  Mode : SIM
  City : Mumbai

══════════════════════════════════════════════════════
  🌤  CURRENT WEATHER – Mumbai, SIM [SIMULATION]
══════════════════════════════════════════════════════
  🌡  Temperature  : 38.5°C  (feels like 42.1°C)
  🔼  High / Low   : 40.5°C / 35.5°C
  💧  Humidity     : 85%
  💨  Wind         : 14.2 m/s  SW
  ☁  Condition    : Heavy Intensity Rain

🚨  WEATHER ALERTS
══════════════════════════════════════════════════════
  🟡 [WARNING] High Temperature: Temperature exceeds threshold (38.5°C)
  🟡 [WARNING] High Humidity: Humidity at 85% – discomfort risk
  🟡 [WARNING] Rain Forecast (Day 5): Expected 22.0 mm rainfall
```

---

## 🔐 Security

- **Never** put your API key directly in Python code.
- Use `.env` file locally — it is in `.gitignore` and **never uploaded**.
- Use `.env.example` (with placeholder values) for GitHub.
- The `reports/` and `outputs/` folders are gitignored to avoid large binary uploads.

---

## 📚 Learning Outcomes

After building this project, you will be able to:
- Integrate REST APIs using `requests` in Python
- Parse and process JSON responses
- Build threshold-based alert systems
- Create data visualisations with `matplotlib`
- Develop interactive dashboards with `streamlit`
- Manage environment variables securely with `python-dotenv`
- Structure a professional Python project for GitHub

---

## 🎓 Interview Talking Points

1. REST API integration and JSON parsing
2. Modular, production-style Python project structure
3. Threshold-based alerting system design
4. Data pipeline: fetch → parse → analyse → visualise → report
5. Secure credential management with environment variables

---

## 📝 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
Built with ❤️ as a Python course project · Ready for GitHub portfolio
</div>
