# controllers/exam_add.py
import sqlite3
import settings

def handle(data, teacher_id):
     conn = None
     try:
          title = data.get('title', [''])[0].strip()
          description = data.get('description', [''])[0].strip()
          duration = data.get('duration', ['30'])[0]
          start_time = data.get('start_time', [''])[0].strip()
          total_score = float(data.get('total_score', ['0'])[0])
          is_random = 1 if data.get('is_random', ['0'])[0] == 'true' else 0
          question_ids = data.get('question_ids', [])
          student_ids = data.get('student_ids', [])

          if not title:
               return "عنوان آزمون الزامی است"
          if not start_time:
               return "زمان شروع آزمون الزامی است"
          if total_score <= 0:
               return "نمره کل باید بزرگتر از صفر باشد"

          if is_random:
               total_q = int(data.get('total_questions', ['0'])[0])
               if total_q <= 0:
                    return "تعداد سوالات برای انتخاب تصادفی الزامی است"
          else:
               if not question_ids or len(question_ids) == 0:
                    return "حداقل یک سوال باید انتخاب شود"
               total_q = len(question_ids)
               conn = sqlite3.connect(str(settings.DB_PATH))
               cursor = conn.cursor()
               total_selected_score = 0
               for qid in question_ids:
                    if qid.isdigit():
                         cursor.execute("SELECT score FROM TBL_questions WHERE id = ?", (int(qid),))
                         row = cursor.fetchone()
                         if row:
                              total_selected_score += row[0]
               conn.close()
               if abs(total_selected_score - total_score) > 0.001:
                    return f"مجموع نمرات سوالات انتخاب شده ({total_selected_score}) با نمره کل ({total_score}) برابر نیست"

          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          sql = '''
               INSERT INTO TBL_exams 
               (teacher_id, title, description, start_time, duration, total_questions, total_score, is_random)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
          '''
          cursor.execute(sql, (teacher_id, title, description, start_time, int(duration), total_q, total_score, is_random))
          exam_id = cursor.lastrowid

          if not is_random:
               for idx, qid in enumerate(question_ids):
                    if qid.isdigit():
                         cursor.execute('''
                         INSERT INTO TBL_exam_questions (exam_id, question_id, order_num)
                         VALUES (?, ?, ?)
                         ''', (exam_id, int(qid), idx))

          for uid in student_ids:
               if uid.isdigit():
                    cursor.execute('''
                         INSERT INTO TBL_exam_users (exam_id, user_id, status)
                         VALUES (?, ?, ?)
                    ''', (exam_id, int(uid), 'pending'))

          conn.commit()
          return "آزمون با موفقیت ساخته شد"
     except Exception as e:
          return f"خطا: {e}"
     finally:
          if conn:
               conn.close()