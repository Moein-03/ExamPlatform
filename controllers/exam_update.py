# controllers/exam_update.py
import sqlite3
import settings

def handle(exam_id, data):
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

          sql = '''UPDATE TBL_exams SET title=?, description=?, start_time=?, duration=? WHERE id=?'''
          cursor.execute(sql, (title, description, start_time, duration, exam_id))
          conn.commit()
          return "آزمون با موفقیت ویرایش شد."
     except Exception as e:
          return f"خطا: {e}"
     finally:
          conn.close()