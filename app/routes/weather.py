from flask import Blueprint, request, jsonify
import json
from app import redis
from app.helpers.weather_fetcher import fetch_current_weather, fetch_forecast
from flask_limiter import Limiter

weather_bp = Blueprint("weather", __name__, url_prefix="/weather")

@weather_bp.route("/", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "El parámetro 'city' es obligatorio"}), 400

    cache_key = f"weather:{city.lower()}"
    cached = redis.get(cache_key)
    if cached:
        return jsonify({"source": "cache", **json.loads(cached)})

    try:
        data = fetch_current_weather(city)
    except Exception as e:
        return jsonify({"error": "Error obteniendo el clima", "details": str(e)}), 502

    redis.set(cache_key, json.dumps(data), ex=43200)
    return jsonify({"source": "api", **data})

@weather_bp.route("/forecast", methods=["GET"])
def get_forecast():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "El parámetro 'city' es obligatorio"}), 400

    cache_key = f"forecast:{city.lower()}"
    cached = redis.get(cache_key)
    if cached:
        return jsonify({"source": "cache", **json.loads(cached)})

    try:
        data = fetch_forecast(city)
    except Exception as e:
        return jsonify({"error": "Error obteniendo el pronóstico", "details": str(e)}), 502

    redis.set(cache_key, json.dumps(data), ex=43200)
    return jsonify({"source": "api", **data})
