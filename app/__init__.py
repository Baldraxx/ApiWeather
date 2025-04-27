from flask import Flask
from redis import Redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config

redis = None
limiter = None

def create_app():
    global redis, limiter
    
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa Redis
    redis = Redis.from_url(app.config["REDIS_URL"], decode_responses=True)

    # Inicializa Rate Limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[app.config["RATE_LIMIT"]]
    )

    # Importa y registra los blueprints (rutas)
    from app.routes.weather import weather_bp
    from app.routes.health import health_bp

    app.register_blueprint(weather_bp)
    app.register_blueprint(health_bp)

    return app
