# controllers/user_update.py
import sqlite3
import settings
import hashlib

def hash_password(password):
     return hashlib.sha256(password.encode()).hexdigest()

def handle(user_id, data):
     if not settings.DB_PATH.exists():
          return "دیتابیس یافت نشد."

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     try:
          fullname = data.get('fullname', [''])[0].strip()
          email = data.get('email', [''])[0].strip()
          role = data.get('role', ['student'])[0]
          university_id = data.get('university_id', [''])[0].strip()
          new_password = data.get('password', [''])[0].strip()

          if not fullname or not email:
               return "نام و ایمیل الزامی است."

          if new_password:
               hashed = hash_password(new_password)
               sql = '''UPDATE TBL_users SET fullname=?, email=?, password=?, role=?, university_id=? WHERE id=?'''
               cursor.execute(sql, (fullname, email, hashed, role, university_id, user_id))
          else:
               sql = '''UPDATE TBL_users SET fullname=?, email=?, role=?, university_id=? WHERE id=?'''
               cursor.execute(sql, (fullname, email, role, university_id, user_id))

          conn.commit()
          return "کاربر با موفقیت به‌روزرسانی شد."
     except sqlite3.IntegrityError:
          return "این ایمیل قبلاً ثبت شده است."
     except Exception as e:
          return f"خطا: {str(e)}"
     finally:
          conn.close()