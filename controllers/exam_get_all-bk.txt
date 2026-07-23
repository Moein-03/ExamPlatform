# controllers/exam_get_all.py
import sqlite3
import settings


def handle(user_id=None, only_published=False):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     query = '''
          SELECT e.*, u.fullname as teacher_name
          FROM TBL_exams e
          LEFT JOIN TBL_users u ON e.teacher_id = u.id
     '''
     params = []
     if only_published:
          query += " WHERE e.is_published = 1"
     query += " ORDER BY e.id DESC"
     cursor.execute(query, params)
     rows = cursor.fetchall()
     conn.close()
     return [dict(row) for row in rows]

""" def handle(teacher_id=None, only_published=False):
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
     return [dict(row) for row in rows] """