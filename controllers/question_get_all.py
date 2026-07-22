# controllers/question_get_all.py
import sqlite3
import settings

def handle(teacher_id=None, exam_id=None):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     if exam_id:
          cursor.execute('''
               SELECT q.*, 
                    (SELECT COUNT(*) FROM TBL_answers WHERE question_id = q.id) as answer_count
               FROM TBL_questions q
               WHERE q.exam_id = ?
               ORDER BY q.id ASC
          ''', (exam_id,))
     elif teacher_id:
          cursor.execute('''
               SELECT q.*, 
                    (SELECT COUNT(*) FROM TBL_answers WHERE question_id = q.id) as answer_count,
                    e.title as exam_title
               FROM TBL_questions q
               LEFT JOIN TBL_exams e ON q.exam_id = e.id
               WHERE e.teacher_id = ? OR q.exam_id IS NULL
               ORDER BY q.id DESC
          ''', (teacher_id,))
     else:
          cursor.execute('''
               SELECT q.*, 
                    (SELECT COUNT(*) FROM TBL_answers WHERE question_id = q.id) as answer_count,
                    e.title as exam_title,
                    u.fullname as teacher_name
               FROM TBL_questions q
               LEFT JOIN TBL_exams e ON q.exam_id = e.id
               LEFT JOIN TBL_users u ON e.teacher_id = u.id
               ORDER BY q.id DESC
          ''')

     rows = cursor.fetchall()
     conn.close()
     return [dict(row) for row in rows]