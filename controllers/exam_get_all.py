# controllers/exam_get_all.py
import sqlite3
import settings

def handle(teacher_id=None, only_published=False):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     query = 'SELECT * FROM exams'
     params = []
     conds = []
     if teacher_id:
          conds.append('teacher_id = ?')
          params.append(teacher_id)
     if only_published:
          conds.append('is_published = 1')
     if conds:
          query += ' WHERE ' + ' AND '.join(conds)
     query += ' ORDER BY created_at DESC'
     cursor.execute(query, params)
     rows = cursor.fetchall()
     dbc.close()
     return [dict(row) for row in rows]