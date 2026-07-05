# controllers/user_get_one.py
import sqlite3
import settings

def handle(user_id):
     if not settings.DB_PATH.exists():
          return None
     
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     try:
          cursor.execute("SELECT id, fullname, email, role, university_id, created_at FROM TBL_users WHERE id = ?", (user_id,))
          row = cursor.fetchone()
          if row:
               return dict(row)
          return None
     except Exception as e:
          print(f"Error in user_get_one: {e}")
          return None
     finally:
          conn.close()