# controllers/exam_add.py
import sqlite3
import settings

def handle(data, teacher_id):
     try:
          title = data.get('title', [''])[0].strip()
          description = data.get('description', [''])[0].strip()
          duration = data.get('duration', ['30'])[0]
          is_random = 1 if data.get('is_random', ['0'])[0] == 'true' else 0
          question_ids = data.get('question_ids', [])
          total = len(question_ids)
          if not title or total == 0:
               return "عنوان و حداقل یک سوال الزامی است"
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          cursor.execute('''
               INSERT INTO exams (teacher_id, title, description, duration, total_questions, is_random)
               VALUES (?, ?, ?, ?, ?, ?)
          ''', (teacher_id, title, description, int(duration), total, is_random))
          exam_id = cursor.lastrowid
          for idx, qid in enumerate(question_ids):
               if qid.isdigit():
                    cursor.execute('''
                         INSERT INTO exam_questions (exam_id, question_id, order_num)
                         VALUES (?, ?, ?)
                    ''', (exam_id, int(qid), idx))
          dbc.commit()
          dbc.close()
          return "آزمون ساخته شد"
     except Exception as e:
          return f"خطا: {e}"