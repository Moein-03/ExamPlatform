# controllers/user_get_one.py
import sqlite3
import settings

def handle(user_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     cursor.execute('''
          SELECT id, firstname, lastname, username, role, created_at
          FROM users WHERE id = ? AND is_deleted = 0
     ''', (user_id,))
     row = cursor.fetchone()
     dbc.close()
     return dict(row) if row else None