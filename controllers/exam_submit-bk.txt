# controllers/exam_submit.py
import sqlite3
import settings

def handle(exam_id, student_id, data):
     try:
          dbc = sqlite3.connect(settings.DB_PATH)
          cursor = dbc.cursor()
          cursor.execute('SELECT * FROM exams WHERE id = ? AND is_published = 1', (exam_id,))
          if not cursor.fetchone():
               dbc.close()
               return "آزمون منتشر نشده است"
          cursor.execute('''
               SELECT id FROM exam_participants
               WHERE exam_id = ? AND student_id = ? AND is_finished = 0
          ''', (exam_id, student_id))
          part = cursor.fetchone()
          if not part:
               cursor.execute('''
                    INSERT INTO exam_participants (exam_id, student_id)
                    VALUES (?, ?)
               ''', (exam_id, student_id))
               participant_id = cursor.lastrowid
          else:
               participant_id = part[0]
          cursor.execute('''
               SELECT q.id, q.question_type, q.correct_answer
               FROM questions q
               JOIN exam_questions eq ON eq.question_id = q.id
               WHERE eq.exam_id = ?
          ''', (exam_id,))
          questions = cursor.fetchall()
          score = 0
          total = len(questions)
          for q in questions:
               q_id = q[0]
               q_type = q[1]
               correct = q[2]
               answer_key = f"question_{q_id}"
               student_answer = data.get(answer_key, [''])[0].strip()
               is_correct = 0
               if q_type == 'multiple_choice':
                    if student_answer == correct:
                         is_correct = 1
               elif q_type == 'fill_blank':
                    if student_answer.strip().lower() == correct.strip().lower():
                         is_correct = 1
               if is_correct:
                    score += 1
               cursor.execute('''
                    INSERT OR REPLACE INTO exam_answers (participant_id, question_id, answer, is_correct)
                    VALUES (?, ?, ?, ?)
               ''', (participant_id, q_id, student_answer, is_correct))
          final_score = (score / total * 100) if total > 0 else 0
          cursor.execute('''
               UPDATE exam_participants
               SET submitted_at = datetime('now'), score = ?, is_finished = 1
               WHERE id = ?
          ''', (final_score, participant_id))
          dbc.commit()
          dbc.close()
          return f"آزمون ثبت شد. نمره: {final_score:.1f}%"
     except Exception as e:
          return f"خطا: {e}"