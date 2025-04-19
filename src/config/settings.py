"""
Module for managing environment variables and configurations.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "123456")
DB_NAME = os.getenv("DB_NAME", "newsAPIgateway")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Application configuration
ALGORITHM = os.getenv("ALGORITHM")
APP_SECRET = os.getenv("APP_SECRET")
APP_EXPIRES_IN = int(os.getenv("APP_EXPIRES_IN", 3600))
REFRESH_TOKEN_EXPIRES_IN = int(os.getenv("REFRESH_TOKEN_EXPIRES_IN", 604800))

# NewsAPI configuration
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", "your-newsapi-api-key")
