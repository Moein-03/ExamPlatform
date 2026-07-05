# controllers/exam_add.py
import sqlite3
import settings

def handle(data):
     if not settings.DB_PATH.exists():
          return "دیتابیس یافت نشد."

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     try:
          title = data.get('title', [''])[0].strip()
          description = data.get('description', [''])[0].strip()
          start_time = data.get('start_time', [''])[0].strip()
          duration = data.get('duration', ['0'])[0].strip()

          if not title:
               return "عنوان آزمون الزامی است."

          sql = '''INSERT INTO TBL_exams (title, description, start_time, duration) VALUES (?, ?, ?, ?)'''
          cursor.execute(sql, (title, description, start_time, duration))
          conn.commit()
          return "آزمون با موفقیت ثبت شد."
     except Exception as e:
          return f"خطا: {e}"
     finally:
          conn.close()