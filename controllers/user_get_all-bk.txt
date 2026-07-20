# controllers/user_get_all.py
import sqlite3
import settings

def handle():
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     cursor.execute('''
          SELECT id, firstname, lastname, username, role, created_at
          FROM users WHERE is_deleted = 0
     ''')
     rows = cursor.fetchall()
     dbc.close()
     return [dict(row) for row in rows]