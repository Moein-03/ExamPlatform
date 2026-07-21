# controllers/question_get_one.py
import sqlite3
import settings

def handle(question_id):
     """
     دریافت یک سوال بر اساس شناسه
     """
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     try:
          cursor.execute('''
               SELECT q.*, 
                    (SELECT COUNT(*) FROM TBL_answers WHERE question_id = q.id) as answer_count,
                    e.title as exam_title,
                    u.fullname as teacher_name
               FROM TBL_questions q
               JOIN TBL_exams e ON q.exam_id = e.id
               LEFT JOIN TBL_users u ON e.teacher_id = u.id
               WHERE q.id = ?
          ''', (question_id,))
          row = cursor.fetchone()
          conn.close()
          return dict(row) if row else None
     except Exception as e:
          print(f"Error in question_get_one: {e}")
          conn.close()
          return None