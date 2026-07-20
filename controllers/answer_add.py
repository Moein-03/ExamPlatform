# controllers/answer_add.py
import sqlite3
import settings

def handle(data):
     """
     افزودن گزینه جدید به یک سوال
     """
     try:
          question_id = int(data.get('question_id', ['0'])[0])
          answer_text = data.get('answer_text', [''])[0].strip()
          is_correct = 1 if data.get('is_correct', ['0'])[0] == '1' else 0
          
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
          return {"success": "گزینه با موفقیت اضافه شد."}
     
     except Exception as e:
          return {"error": str(e)}