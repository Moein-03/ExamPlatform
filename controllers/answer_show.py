# controllers/answer_show.py
import sqlite3
import settings

def handle(question_id):
     """
     دریافت گزینه‌های یک سوال (برای نمایش در فرم ویرایش سوال)
     """
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     try:
          cursor.execute('''
               SELECT * FROM TBL_answers
               WHERE question_id = ?
               ORDER BY id ASC
          ''', (question_id,))
          rows = cursor.fetchall()
          conn.close()
          return [dict(row) for row in rows]
     except Exception as e:
          print(f"Error in answer_show: {e}")
          conn.close()
          return []