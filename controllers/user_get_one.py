# controllers/user_get_one.py
import sqlite3
import settings

def handle(user_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     try:
          cursor.execute("SELECT * FROM TBL_users WHERE id = ?", (user_id))
          row = cursor.fetchone()
          return dict(row) if row else None
     finally:
          conn.close()