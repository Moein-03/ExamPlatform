# controllers/question_update.py
import sqlite3
import settings

def handle(question_id, data):
     conn = None
     try:
          question_text = data.get('question_text', [''])[0].strip()
          question_type = data.get('question_type', ['true_false'])[0]
          score = float(data.get('score', ['1'])[0])
          answers = data.get('answers', [])

          if not question_text:
               return "متن سوال الزامی است."

          valid_types = ['true_false', 'single', 'descriptive']
          if question_type not in valid_types:
               question_type = 'true_false'

          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()

          cursor.execute('''
               UPDATE TBL_questions
               SET question_text = ?, question_type = ?, score = ?
               WHERE id = ?
          ''', (question_text, question_type, score, question_id))

          # فقط اگر answers خالی نباشد، گزینه‌ها را به‌روز کن
          if answers and question_type in ['true_false', 'single']:
               # حذف گزینه‌های قبلی
               cursor.execute("DELETE FROM TBL_answers WHERE question_id = ?", (question_id,))
               
               if question_type == 'true_false':
                    if len(answers) != 2:
                         return "برای سوال صحیح/غلط دقیقاً دو گزینه نیاز است."
                    correct_count = sum(1 for ans in answers if ans.get('is_correct', False))
                    if correct_count != 1:
                         return "در سوال صحیح/غلط فقط یکی از گزینه‌ها باید صحیح باشد."
               elif question_type == 'single':
                    if len(answers) < 2:
                         return "برای سوال چند گزینه‌ای حداقل دو گزینه نیاز است."
                    correct_count = sum(1 for ans in answers if ans.get('is_correct', False))
                    if correct_count != 1:
                         return "در سوال چند گزینه‌ای فقط یک گزینه باید صحیح باشد."

               for ans in answers:
                    answer_text = ans.get('text', '').strip()
                    is_correct = 1 if ans.get('is_correct', False) else 0
                    if answer_text:
                         cursor.execute('''
                         INSERT INTO TBL_answers (question_id, answer_text, is_correct)
                         VALUES (?, ?, ?)
                         ''', (question_id, answer_text, is_correct))

          conn.commit()
          return "سوال با موفقیت ویرایش شد."
     except Exception as e:
          return f"خطا: {e}"
     finally:
          if conn:
               conn.close()