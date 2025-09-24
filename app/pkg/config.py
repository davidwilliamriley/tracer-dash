# config.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

env_db = os.getenv("DB_PATH")
DB_PATH = Path(env_db) if env_db else (DATA_DIR / "db.sqlite3")

DATABASE_CONFIG = {
    "database": str(DB_PATH)
    }

APP_CONFIG = {
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "host": os.getenv("HOST", "127.0.0.1"),
    "port": int(os.getenv("PORT", "8050")),
    "title": os.getenv("APP_TITLE", "Dash MVC Example")
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
