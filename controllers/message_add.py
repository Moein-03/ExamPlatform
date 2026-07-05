# controllers/message_add.py
import sqlite3
import settings

def handle(data):
     if not settings.DB_PATH.exists():
          return "دیتابیس یافت نشد. ابتدا /setup را اجرا کنید."

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     try:
          user_name = data.get('user_name', [''])[0].strip()
          user_email = data.get('user_email', [''])[0].strip()
          subject = data.get('subject', [''])[0].strip()
          user_message = data.get('user_message', [''])[0].strip()

          if not user_name or not user_email or not user_message:
               return "نام، ایمیل و متن پیام الزامی است."

          sql = '''INSERT INTO TBL_messages (user_name, user_email, user_message, subject) VALUES (?, ?, ?, ?)'''
          cursor.execute(sql, (user_name, user_email, user_message, subject))
          conn.commit()
          return "پیام با موفقیت ارسال شد."
     except Exception as e:
          return f"خطا: {e}"
     finally:
          conn.close()