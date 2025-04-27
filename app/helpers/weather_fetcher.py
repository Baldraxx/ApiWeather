import requests
import time
from flask import current_app

def fetch_current_weather(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}"
    params = {
        "unitGroup": "metric",
        "key": current_app.config["VC_API_KEY"],
        "include": "current",
        "elements": "temp,humidity,conditions"
    }
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    current = data.get("currentConditions", {})
    return {
        "location": data.get("address"),
        "temp": current.get("temp"),
        "humidity": current.get("humidity"),
        "conditions": current.get("conditions"),
        "timestamp": int(time.time())
    }

def fetch_forecast(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={current_app.config['VC_API_KEY']}&include=days"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    forecast = []
    for day in data.get("days", [])[:3]:  # Solo los próximos 3 días
        forecast.append({
            "date": day.get("datetime"),
            "tempmax": day.get("tempmax"),
            "tempmin": day.get("tempmin"),
            "conditions": day.get("conditions")
        })
    return {
        "location": data.get("address"),
        "forecast": forecast,
        "timestamp": int(time.time())
    }
