# settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = 'examPlatform_database.db'
DB_PATH = BASE_DIR / DB_NAME
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_URL_PREFIX = "/static/"

BASE_URL = '/ExamPlatform'