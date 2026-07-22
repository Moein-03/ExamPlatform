# controllers/question_add.py
import sqlite3
import settings

def handle(data, exam_id):
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

          if exam_id == 0 or exam_id is None:
               cursor.execute('''
                    INSERT INTO TBL_questions (question_text, question_type, score)
                    VALUES (?, ?, ?)
               ''', (question_text, question_type, score))
          else:
               cursor.execute('''
                    INSERT INTO TBL_questions (exam_id, question_text, question_type, score)
                    VALUES (?, ?, ?, ?)
               ''', (exam_id, question_text, question_type, score))

          question_id = cursor.lastrowid

          if question_type in ['true_false', 'single']:
               if not answers:
                    return "برای سوال تستی حداقل یک گزینه الزامی است."
               
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
          return "سوال با موفقیت اضافه شد."
     except Exception as e:
          return f"خطا: {e}"
     finally:
          if conn:
               conn.close()

#def handle(data, exam_id):
#     conn = None
#     try:
#          question_text = data.get('question_text', [''])[0].strip()
#          question_type = data.get('question_type', ['true_false'])[0]
#          score = float(data.get('score', ['1'])[0])
#          answers = data.get('answers', [])

#          if not question_text:
#               return "متن سوال الزامی است."

#          conn = sqlite3.connect(str(settings.DB_PATH))
#          cursor = conn.cursor()

#          if exam_id == 0 or exam_id is None:
#               cursor.execute('''
#                    INSERT INTO TBL_questions (question_text, question_type, score)
#                    VALUES (?, ?, ?)
#               ''', (question_text, question_type, score))
#          else:
#               cursor.execute('''
#                    INSERT INTO TBL_questions (exam_id, question_text, question_type, score)
#                    VALUES (?, ?, ?, ?)
#               ''', (exam_id, question_text, question_type, score))

#          question_id = cursor.lastrowid

#          if question_type == 'true_false' or question_type == 'multiple':
#               if not answers:
#                    return "برای سوال تستی حداقل یک گزینه الزامی است."

#               if question_type == 'true_false':
#                    found_correct = False
#                    for ans in answers:
#                         if ans.get('is_correct', False):
#                              if not found_correct:
#                                   found_correct = True
#                              else:
#                                   ans['is_correct'] = False

#               for ans in answers:
#                    answer_text = ans.get('text', '').strip()
#                    is_correct = 1 if ans.get('is_correct', False) else 0
#                    if answer_text:
#                         cursor.execute('''
#                         INSERT INTO TBL_answers (question_id, answer_text, is_correct)
#                         VALUES (?, ?, ?)
#                         ''', (question_id, answer_text, is_correct))

#          conn.commit()
#          return "سوال با موفقیت اضافه شد."
#     except Exception as e:
#          return f"خطا: {e}"
#     finally:
#          if conn:
#               conn.close()