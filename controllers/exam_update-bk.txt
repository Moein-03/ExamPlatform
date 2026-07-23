# controllers/exam_update.py
import sqlite3
import settings

def handle(exam_id, data, teacher_id):
     try:
          title = data.get('title', [''])[0].strip()
          description = data.get('description', [''])[0].strip()
          duration = data.get('duration', ['30'])[0]
          is_published = 1 if data.get('is_published', ['0'])[0] in ['1', 'true'] else 0
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          cursor.execute('SELECT teacher_id FROM exams WHERE id = ?', (exam_id,))
          row = cursor.fetchone()
          if not row or row[0] != teacher_id:
               dbc.close()
               return "دسترسی ندارید"
          cursor.execute('''
               UPDATE exams SET title=?, description=?, duration=?, is_published=?
               WHERE id=?
          ''', (title, description, int(duration), is_published, exam_id))
          dbc.commit()
          dbc.close()
          return "آزمون ویرایش شد"
     except Exception as e:
          return f"خطا: {e}"