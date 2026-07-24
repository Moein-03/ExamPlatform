# controllers/user_update_role.py
import sqlite3
import settings

def handle(user_id, data):
     try:
          new_role = data.get('role', ['student'])[0].strip()
          if new_role not in ['admin', 'teacher', 'student']:
               return "نقش نامعتبر است"
          
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          query = '''
               UPDATE TBL_users
               SET role = ?
               WHERE id = ?
          '''
          cursor.execute(query, (new_role, user_id))
          conn.commit()
          conn.close()
          return "نقش کاربر تغییر کرد"
     except Exception as e:
          return f"خطا: {e}"