# 🚀 GitHub Upload Steps

## Create Repository
1. Go to https://github.com/new
2. Name: `Weather-Forecast-Alert-Application`
3. Description: `Python weather app with live API, simulation, smart alerts, charts & Streamlit dashboard`
4. Public · No README · No .gitignore (you have them)

## Connect & Push
```bash
cd Weather-Forecast-Alert-Application
git init
git remote add origin https://github.com/YOUR_USERNAME/Weather-Forecast-Alert-Application.git
git add .
git commit -m "feat: initial project setup"
git branch -M main
git push -u origin main
```

## Day-wise Commits
| Day | Commit message |
|---|---|
| 1 | chore: project setup and dependencies |
| 2 | feat: add API integration and simulation mode |
| 3 | feat: add JSON parsing and terminal display |
| 4 | feat: implement weather alert system |
| 5 | feat: add matplotlib charts and reports |
| 6 | docs: Streamlit dashboard and complete README |

## Tags
`python` `weather-api` `openweathermap` `streamlit` `matplotlib` `data-visualization` `alert-system` `portfolio`

## Never Upload
- .env (real API key)
- venv/
- __pycache__/
