# controllers/exam_results.py
import sqlite3
import settings

def handle(exam_id, student_id=None):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     if student_id:
          cursor.execute('''
               SELECT ep.*, u.firstname, u.lastname
               FROM exam_participants ep
               JOIN users u ON u.id = ep.student_id
               WHERE ep.exam_id = ? AND ep.student_id = ?
          ''', (exam_id, student_id))
     else:
          cursor.execute('''
               SELECT ep.*, u.firstname, u.lastname
               FROM exam_participants ep
               JOIN users u ON u.id = ep.student_id
               WHERE ep.exam_id = ? AND ep.is_finished = 1
               ORDER BY ep.score DESC
          ''', (exam_id,))
     rows = cursor.fetchall()
     dbc.close()
     return [dict(row) for row in rows]