# controllers/user_update_role.py
import sqlite3
import settings

def handle(user_id, data):
     try:
          new_role = data.get('role', ['0'])[0]
          if not new_role.isdigit():
               return "نقش نامعتبر است"
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          cursor.execute('''
               UPDATE users SET role = ? WHERE id = ? AND is_deleted = 0
          ''', (int(new_role), user_id))
          dbc.commit()
          dbc.close()
          return "نقش کاربر تغییر کرد"
     except Exception as e:
          return f"خطا: {e}"