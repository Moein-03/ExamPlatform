# controllers/exam_delete.py
import sqlite3
import settings

def handle(exam_id, teacher_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     cursor = dbc.cursor()
     cursor.execute('SELECT teacher_id FROM exams WHERE id = ?', (exam_id,))
     row = cursor.fetchone()
     if not row or row[0] != teacher_id:
          dbc.close()
          return "دسترسی ندارید"
     cursor.execute('DELETE FROM exam_questions WHERE exam_id = ?', (exam_id,))
     cursor.execute('DELETE FROM exam_participants WHERE exam_id = ?', (exam_id,))
     cursor.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
     dbc.commit()
     dbc.close()
     return "آزمون حذف شد"