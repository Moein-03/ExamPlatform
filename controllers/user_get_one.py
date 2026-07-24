# controllers/user_get_one.py
import sqlite3
import settings

def handle(user_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     query = '''
          SELECT id, fullname, email, role, university_id, created_at
          FROM TBL_users
          WHERE id = ?
     '''
     cursor.execute(query, (user_id,))
     row = cursor.fetchone()
     conn.close()
     return dict(row) if row else None