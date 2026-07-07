# controllers/user_login.py
import sqlite3
import settings

def handle(data):
     username = data.get('username', [''])[0].strip()
     password = data.get('password', [''])[0].strip()
     if not username or not password:
          return None
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     cursor.execute('''
          SELECT * FROM users
          WHERE username = ? AND password = ? AND is_deleted = 0
     ''', (username, password))
     row = cursor.fetchone()
     dbc.close()
     return dict(row) if row else None