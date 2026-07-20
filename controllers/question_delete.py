# controllers/question_delete.py
import sqlite3
import settings

def handle(question_id, user_id=None):
     """
     حذف سوال (با بررسی دسترسی)
     """
     try:
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          
          # اگر user_id داده شده، بررسی کن که سوال متعلق به آزمون استاد است
          if user_id:
               cursor.execute('''
                    SELECT q.id FROM TBL_questions q
                    JOIN TBL_exams e ON q.exam_id = e.id
                    WHERE q.id = ? AND e.teacher_id = ?
               ''', (question_id, user_id))
               if not cursor.fetchone():
                    conn.close()
                    return "شما دسترسی حذف این سوال را ندارید."
          
          # حذف گزینه‌های سوال (به دلیل FOREIGN KEY با ON DELETE CASCADE، خودکار حذف می‌شوند)
          cursor.execute("DELETE FROM TBL_questions WHERE id = ?", (question_id,))
          conn.commit()
          conn.close()
          return "سوال با موفقیت حذف شد."
     
     except Exception as e:
          return f"خطا: {e}"