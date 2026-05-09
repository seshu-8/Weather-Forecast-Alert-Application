# 🎤 Interview Preparation – Weather Forecast & Alert Application

## Q1. Explain your project.

**HR Answer:**
"I built a Weather Forecast & Alert Application in Python. It connects to the OpenWeatherMap API to fetch live weather data for any city, analyses conditions, generates smart alerts, creates charts, and saves reports. It also has a Streamlit web dashboard. It has two modes — live API and offline simulation."

**Technical Answer:**
"The application uses modular Python. `weather_api.py` handles HTTP requests to OpenWeatherMap and normalises the JSON response. `alert_system.py` applies configurable thresholds and generates Alert dataclass objects with CRITICAL/WARNING/INFO severity. `visualizer.py` uses matplotlib for 4 dark-themed charts. `dashboard.py` is a Streamlit app with threshold sliders and CSV/TXT export. API keys are secured via python-dotenv."

---

## Q2. What is an API and how does your project use it?

"An API lets two systems communicate. I send an HTTP GET to OpenWeatherMap with the city and API key. It returns JSON with weather data which I parse using Python dicts. This is how all weather apps work."

---

## Q3. Why did you build a simulation mode?

"As a student, I may not always have an API key or internet. Simulation mode uses pre-defined JSON data to run the full pipeline — alerts, charts, reports, and dashboard. It also taught me to make the code data-source agnostic."

---

## Q4. How does your alert system work?

"The alert system has configurable thresholds. For each condition — temperature, humidity, wind, rain, weather description — I compare values to thresholds. Each alert is a dataclass with level, category, message, and value. I also scan the forecast to generate proactive alerts for upcoming bad weather."

---

## Q5. How did you handle API errors?

"I used try-except blocks handling ConnectionError (no internet), HTTPError (401 invalid key / 404 city not found), and 10s timeout. Each raises a meaningful exception guiding the user."

---

## Q6. Explain the data flow in your project.

"6 stages: Input → Fetch (API/simulation) → Parse (JSON to dict) → Analyse (alert logic) → Visualise (matplotlib charts) → Report (CSV + TXT files)."

---

## Q7. How did you secure your API key?

"Using python-dotenv. Key is in .env which is gitignored. GitHub has .env.example with a placeholder. This is the industry-standard 12-Factor App pattern."

---

## Q8. What visualisations did you create?

"4 charts: temperature line (max/min), humidity bar with threshold line, rainfall bar coloured by intensity, wind speed line. Plus a 4-panel dashboard PNG. All use a dark theme for readability."

---

## Q9. What would you add next?

"Email/SMS alerts via smtplib/Twilio, SQLite database for history, multi-city comparison, ML temperature prediction with scikit-learn, and a FastAPI backend."

---

## Q10. What did you learn?

"REST API integration, JSON parsing, modular Python structure, alert system design, matplotlib charts, Streamlit dashboards, secure credential management, and professional GitHub documentation."
