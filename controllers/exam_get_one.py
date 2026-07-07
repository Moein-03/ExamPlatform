# controllers/exam_get_one.py
import sqlite3
import settings

def handle(exam_id, teacher_id=None, only_published=False):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     query = 'SELECT * FROM exams WHERE id = ?'
     params = [exam_id]
     if teacher_id:
          query += ' AND teacher_id = ?'
          params.append(teacher_id)
     if only_published:
          query += ' AND is_published = 1'
     cursor.execute(query, params)
     row = cursor.fetchone()
     dbc.close()
     return dict(row) if row else None