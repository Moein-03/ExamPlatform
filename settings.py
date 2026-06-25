# settings.py
from pathlib import Path
import importlib.util

DB_NAME = 'examPlatform_database.db'
BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / DB_NAME
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_URL_PREFIX = "/static/"