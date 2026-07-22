# controllers/question_get_one.py
import sqlite3
import settings

def handle(question_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     cursor.execute('''
          SELECT q.*, 
                    (SELECT COUNT(*) FROM TBL_answers WHERE question_id = q.id) as answer_count,
                    e.title as exam_title
          FROM TBL_questions q
          LEFT JOIN TBL_exams e ON q.exam_id = e.id
          WHERE q.id = ?
     ''', (question_id,))
     row = cursor.fetchone()
     conn.close()
     return dict(row) if row else None