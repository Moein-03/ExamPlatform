import sqlite3
import settings

def handle(exam_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     cursor.execute("""
          SELECT id, title, description, exam_date, start_time, duration_min,
                    question_count, total_score, category, status
          FROM TBL_exams WHERE id = ?
     """, (exam_id,))
     row = cursor.fetchone()
     conn.close()
     if row:
          return dict(row)
     return None