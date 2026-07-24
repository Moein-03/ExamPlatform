# controllers/exam_results.py
import sqlite3
import settings

def handle(exam_id, student_id=None):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     
     if student_id:
          query = '''
               SELECT eu.*, u.fullname, u.email
               FROM TBL_exam_users eu
               JOIN TBL_users u ON u.id = eu.user_id
               WHERE eu.exam_id = ? AND eu.user_id = ?
          '''
          cursor.execute(query, (exam_id, student_id))
          row = cursor.fetchone()
          conn.close()
          if not row:
               return None
          result = dict(row)
          result['passed'] = result.get('score', 0) >= 50
          return result
     else:
          query = '''
               SELECT eu.*, u.fullname, u.email
               FROM TBL_exam_users eu
               JOIN TBL_users u ON u.id = eu.user_id
               WHERE eu.exam_id = ? AND eu.status = 'completed'
               ORDER BY eu.score DESC
          '''
          cursor.execute(query, (exam_id,))
          rows = cursor.fetchall()
          conn.close()
          return [dict(row) for row in rows]