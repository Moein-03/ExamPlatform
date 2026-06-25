import sqlite3
import os


def handle():
     if not settings.DB_PATH.exists():
          print(f"فایل دیتابیس در مسیر {settings.DB_PATH} یافت نشد. ابتدا db_setup.py را اجرا کنید.")
          return

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()

     try:
          # درج در جدول پیام های فرم تماس با ما
          message_data = ('رضا کریمی', 'reza.karimi@example.com', 'مشکل در ورود به آزمون', 'مشکل فنی')
          
          sql = '''
               INSERT INTO TBL_messages (user_name, user_email, user_message, subject)
               VALUES (?, ?, ?, ?)
          '''
          cursor.execute(sql, message_data)
          conn.commit()
          print("پیام با موفقیت درج شد.")

     except Exception as e:
          print(f"خطا: {e}")

     finally:
          conn.close()

if __name__ == '__main__':
    handle()