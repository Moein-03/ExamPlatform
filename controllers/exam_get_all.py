# controllers/exam_get_all.py
import sqlite3
import settings

def handle(user_id=None, only_published=False, student_id=None):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     query = '''
          SELECT e.*, u.fullname as teacher_name
          FROM TBL_exams e
          LEFT JOIN TBL_users u ON e.teacher_id = u.id
     '''
     params = []
     conditions = []

     if student_id:
          query = '''
               SELECT e.*, u.fullname as teacher_name
               FROM TBL_exams e
               LEFT JOIN TBL_users u ON e.teacher_id = u.id
               JOIN TBL_exam_users eu ON e.id = eu.exam_id
               WHERE eu.user_id = ?
          '''
          params.append(student_id)

     if only_published:
          if student_id:
               query += " AND e.is_published = 1"
          else:
               query += " WHERE e.is_published = 1"

     query += " ORDER BY e.id DESC"
     cursor.execute(query, params)
     rows = cursor.fetchall()
     conn.close()
     return [dict(row) for row in rows]