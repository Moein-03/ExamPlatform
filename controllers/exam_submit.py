# controllers/exam_submit.py
import sqlite3
import settings

def handle(exam_id, student_id, data):
     conn = None
     try:
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()

          cursor.execute("SELECT id, duration, start_time FROM TBL_exams WHERE id = ? AND is_published = 1", (exam_id,))
          exam = cursor.fetchone()
          if not exam:
               return "آزمون منتشر نشده است یا وجود ندارد"

          cursor.execute("SELECT id, status FROM TBL_exam_users WHERE exam_id = ? AND user_id = ?", (exam_id, student_id))
          participant = cursor.fetchone()
          if not participant:
               return "شما در این آزمون ثبت‌نام نشده‌اید"
          if participant[1] == 'completed':
               return "شما قبلاً در این آزمون شرکت کرده‌اید"

          cursor.execute('''
               SELECT q.id, q.question_type, a.answer_text as correct_answer
               FROM TBL_questions q
               JOIN TBL_exam_questions eq ON eq.question_id = q.id
               LEFT JOIN TBL_answers a ON a.question_id = q.id AND a.is_correct = 1
               WHERE eq.exam_id = ?
               ORDER BY eq.order_num
          ''', (exam_id,))
          questions = cursor.fetchall()

          total_score = 0
          total_questions = len(questions)

          for q in questions:
               q_id = q[0]
               q_type = q[1]
               correct = q[2] if q[2] else ''
               answer_key = f"question_{q_id}"
               student_answer = data.get(answer_key, [''])[0].strip() if isinstance(data.get(answer_key), list) else data.get(answer_key, '')

               is_correct = 0
               if q_type in ['single', 'true_false']:
                    if student_answer == correct:
                         is_correct = 1
               elif q_type == 'descriptive':
                    # برای سوالات تشریحی، فعلاً 0.5 نمره به ازای پاسخ غیرخالی
                    if student_answer:
                         is_correct = 0.5

               cursor.execute('''
                    INSERT OR REPLACE INTO TBL_exam_users (exam_id, user_id, status, score)
                    VALUES (?, ?, ?, ?)
               ''', (exam_id, student_id, 'completed', 0))  # موقتاً 0، بعداً به‌روز می‌شود

               if is_correct:
                    total_score += 1

          # محاسبه نمره نهایی (از ۱۰۰)
          final_score = (total_score / total_questions * 100) if total_questions > 0 else 0

          cursor.execute('''
               UPDATE TBL_exam_users
               SET score = ?, status = 'completed', completed_at = datetime('now')
               WHERE exam_id = ? AND user_id = ?
          ''', (final_score, exam_id, student_id))

          conn.commit()
          return f"آزمون با موفقیت ثبت شد. نمره شما: {final_score:.1f}%"

     except Exception as e:
          return f"خطا: {e}"
     finally:
          if conn:
               conn.close()