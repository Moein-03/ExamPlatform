# controllers/exam_get_one.py
import sqlite3
import settings

def handle(exam_id, teacher_id=None, only_published=False):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     if teacher_id:
          cursor.execute("SELECT * FROM TBL_exams WHERE id = ? AND teacher_id = ?", (exam_id, teacher_id))
     elif only_published:
          cursor.execute("SELECT * FROM TBL_exams WHERE id = ? AND is_published = 1", (exam_id,))
     else:
          cursor.execute("SELECT * FROM TBL_exams WHERE id = ?", (exam_id,))
     
     row = cursor.fetchone()
     if not row:
          conn.close()
          return None
     exam = dict(row)

     cursor.execute("SELECT question_id FROM TBL_exam_questions WHERE exam_id = ? ORDER BY order_num", (exam_id,))
     rows = cursor.fetchall()
     exam['question_ids'] = [r['question_id'] for r in rows]

     cursor.execute("SELECT user_id FROM TBL_exam_users WHERE exam_id = ?", (exam_id,))
     rows = cursor.fetchall()
     exam['student_ids'] = [r['user_id'] for r in rows]
     
     conn.close()
     return exam