# controllers/answer_get_by_question.py
import sqlite3
import settings

def handle(question_id):
     """
     دریافت تمام گزینه‌های یک سوال بر اساس شناسه سوال
     """
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     try:
          cursor.execute('''
               SELECT id, question_id, answer_text, is_correct, created_at
               FROM TBL_answers
               WHERE question_id = ?
               ORDER BY id ASC
          ''', (question_id,))
          rows = cursor.fetchall()
          conn.close()
          return [dict(row) for row in rows]
     except Exception as e:
          print(f"Error in answer_get_by_question: {e}")
          conn.close()
          return []