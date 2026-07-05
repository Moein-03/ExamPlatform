# controllers/exam_get_one.py
import sqlite3
import settings

def handle(exam_id):
     if not settings.DB_PATH.exists():
          return None
     
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     try:
          cursor.execute("SELECT id, title, description, start_time, duration FROM TBL_exams WHERE id = ?", (exam_id,))
          row = cursor.fetchone()
          if row:
               return dict(row)
          return None
     except Exception as e:
          print(f"Error in exam_get_one: {e}")
          return None
     finally:
          conn.close()