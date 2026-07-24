# controllers/exam_update.py
import sqlite3
import settings

def handle(exam_id, data, teacher_id):
     conn = None
     try:
          title = data.get('title', [''])[0].strip() if data.get('title') else None
          description = data.get('description', [''])[0].strip() if data.get('description') else None
          duration = data.get('duration', ['30'])[0] if data.get('duration') else None
          start_time = data.get('start_time', [''])[0].strip() if data.get('start_time') else None
          total_score = float(data.get('total_score', ['0'])[0]) if data.get('total_score') else None
          #is_random = 1 if data.get('is_random', ['0'])[0] == 'true' else 0
          is_random = False
          is_published = int(data.get('is_published', ['0'])[0])
          question_ids = data.get('question_ids', [])
          student_ids = data.get('student_ids', [])

          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()

          if title is None:
               cursor.execute('''
                    UPDATE TBL_exams
                    SET is_published = ?
                    WHERE id = ? AND teacher_id = ?
               ''', (is_published, exam_id, teacher_id))
               conn.commit()
               return "وضعیت آزمون تغییر کرد"

          if not title:
               return "عنوان آزمون الزامی است"
          if not start_time:
               return "زمان شروع آزمون الزامی است"
          if total_score and total_score <= 0:
               return "نمره کل باید بزرگتر از صفر باشد"

          total_q = len(question_ids) if question_ids else 0
          if total_q == 0:
               return "حداقل یک سوال باید انتخاب شود"

          if question_ids:
               total_selected_score = 0
               for qid in question_ids:
                    if qid.isdigit():
                         cursor.execute("SELECT score FROM TBL_questions WHERE id = ?", (int(qid),))
                         row = cursor.fetchone()
                         if row:
                              total_selected_score += row[0]
               if total_selected_score != total_score:
                    return f"مجموع نمرات سوالات ({total_selected_score}) با نمره کل ({total_score}) برابر نیست"

          cursor.execute('''
               UPDATE TBL_exams
               SET title=?, description=?, start_time=?, duration=?, 
                    total_questions=?, total_score=?, is_random=?, is_published=?
               WHERE id=? AND teacher_id=?
          ''', (title, description or '', start_time, int(duration), 
               total_q, total_score, is_random, is_published, exam_id, teacher_id))

          cursor.execute("DELETE FROM TBL_exam_questions WHERE exam_id = ?", (exam_id,))
          cursor.execute("DELETE FROM TBL_exam_users WHERE exam_id = ?", (exam_id,))

          #if not is_random:
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
          return "آزمون با موفقیت ویرایش شد"
     except Exception as e:
          return f"خطا: {e}"
     finally:
          if conn:
               conn.close()