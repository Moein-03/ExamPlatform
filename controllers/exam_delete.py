# controllers/exam_delete.py
import sqlite3
import settings

def handle(exam_id, teacher_id=None):
     conn = None
     try:
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()

          if teacher_id:
               cursor.execute("SELECT id FROM TBL_exams WHERE id = ? AND teacher_id = ?", (exam_id, teacher_id))
               if not cursor.fetchone():
                    return "شما دسترسی حذف این آزمون را ندارید."

          cursor.execute("DELETE FROM TBL_exams WHERE id = ?", (exam_id,))
          conn.commit()
          return "آزمون با موفقیت حذف شد."
     except Exception as e:
          return f"خطا در حذف آزمون: {e}"
     finally:
          if conn:
               conn.close()