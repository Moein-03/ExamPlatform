# controllers/question_add.py
import sqlite3
import settings
import json

def handle(data, teacher_id):
     try:
          question_text = data.get('question_text', [''])[0].strip()
          q_type = data.get('question_type', ['multiple_choice'])[0]
          correct = data.get('correct_answer', [''])[0].strip()
          difficulty = data.get('difficulty', ['1'])[0]
          if not question_text or not correct:
               return "متن سوال و پاسخ صحیح الزامی است"
          options = None
          if q_type == 'multiple_choice':
               opts = data.get('options', [])
               if opts:
                    options = json.dumps(opts)
               else:
                    return "گزینه‌ها را وارد کنید"
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          cursor.execute('''
               INSERT INTO questions (teacher_id, question_text, question_type, options, correct_answer, difficulty)
               VALUES (?, ?, ?, ?, ?, ?)
          ''', (teacher_id, question_text, q_type, options, correct, int(difficulty)))
          dbc.commit()
          dbc.close()
          return "سوال اضافه شد"
     except Exception as e:
          return f"خطا: {e}"