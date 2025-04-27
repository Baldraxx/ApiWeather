import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VC_API_KEY = os.getenv("VC_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL")
    CACHE_TTL = int(os.getenv("CACHE_TTL", 43200)) # 12 horas por defecto
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/hour")
