# controllers/question_import.py
import sqlite3
import settings
import json

def handle(data, teacher_id):
     try:
          json_data = data.get('questions_json', [''])[0]
          if not json_data:
               return "داده‌ای وارد نشده"
          questions = json.loads(json_data)
          if not isinstance(questions, list):
               return "فرمت نامعتبر"
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          count = 0
          for q in questions:
               q_text = q.get('question_text', '').strip()
               q_type = q.get('question_type', 'multiple_choice')
               correct = q.get('correct_answer', '').strip()
               difficulty = q.get('difficulty', 1)
               opts = q.get('options', [])
               if not q_text or not correct:
                    continue
               opts_json = json.dumps(opts) if opts else None
               query = '''
                    INSERT INTO questions (teacher_id, question_text, question_type, options, correct_answer, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?)
               '''
               cursor.execute(query, (teacher_id, q_text, q_type, opts_json, correct, difficulty))
               count += 1
          dbc.commit()
          dbc.close()
          return f"{count} سوال بارگذاری شد"
     except Exception as e:
          return f"خطا: {e}"