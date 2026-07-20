# controllers/question_update.py
import sqlite3
import settings

def handle(question_id, data):
     """
     ویرایش سوال موجود
     """
     try:
          question_text = data.get('question_text', [''])[0].strip()
          question_type = data.get('question_type', ['single'])[0]
          score = float(data.get('score', ['1'])[0])
          
          if not question_text:
               return "متن سوال الزامی است."
          
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          
          cursor.execute('''
               UPDATE TBL_questions
               SET question_text = ?, question_type = ?, score = ?
               WHERE id = ?
          ''', (question_text, question_type, score, question_id))
          
          conn.commit()
          conn.close()
          return "سوال با موفقیت ویرایش شد."
     
     except Exception as e:
          return f"خطا: {e}"