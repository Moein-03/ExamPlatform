# controllers/answer_get_by_question.py
import sqlite3
import settings

def handle(question_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     cursor.execute('''
          SELECT * FROM TBL_answers
          WHERE question_id = ?
          ORDER BY id ASC
     ''', (question_id,))
     rows = cursor.fetchall()
     conn.close()
     return [dict(row) for row in rows]