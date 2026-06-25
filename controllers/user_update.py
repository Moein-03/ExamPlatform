import sqlite3
from urllib.parse import parse_qs
import settings

def handle(user_id, body):
     params = parse_qs(body)
     fullname = params.get('fullname', [''])[0].strip()
     email = params.get('email', [''])[0].strip()
     role = params.get('role', [''])[0].strip()
     university_id = params.get('university_id', [''])[0].strip()

     if not fullname or not email:
          return "نام و ایمیل الزامی است"

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     try:
          cursor.execute("""
               UPDATE TBL_users 
               SET fullname = ?, email = ?, role = ?, university_id = ?
               WHERE id = ?
          """, (fullname, email, role, university_id, user_id))
          conn.commit()
          return f"کاربر با شناسه {user_id} با موفقیت ویرایش شد."
     except Exception as e:
          return f"خطا در ویرایش: {e}"
     finally:
          conn.close()