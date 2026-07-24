# controllers/user_delete.py
import sqlite3
import settings

def handle(user_id):
     try:
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          cursor.execute("DELETE FROM TBL_users WHERE id = ?", (user_id,))
          conn.commit()
          conn.close()
          return "کاربر با موفقیت حذف شد."
     except Exception as e:
          return f"خطا در حذف کاربر: {e}"