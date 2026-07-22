# controllers/answer_add.py
import sqlite3
import settings
import json

def handle(data, question_id):
     try:
          answer_text = data.get('answer_text', '').strip()
          is_correct = int(data.get('is_correct', 0))
          if not answer_text:
               return {"error": "متن گزینه الزامی است."}
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          cursor.execute('''
               INSERT INTO TBL_answers (question_id, answer_text, is_correct)
               VALUES (?, ?, ?)
          ''', (question_id, answer_text, is_correct))
          conn.commit()
          conn.close()
          return {"success": True}
     except Exception as e:
          return {"error": str(e)}