# controllers/user_get_all.py
import sqlite3
import settings

def handle(role=None):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     if role:
          cursor.execute("SELECT id, fullname, email, role, university_id, created_at FROM TBL_users WHERE role = ? ORDER BY id DESC", (role,))
     else:
          cursor.execute("SELECT id, fullname, email, role, university_id, created_at FROM TBL_users ORDER BY id DESC")
     rows = cursor.fetchall()
     conn.close()
     return [dict(row) for row in rows]