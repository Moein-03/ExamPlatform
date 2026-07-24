# controllers/question_get_by_exam.py
import sqlite3
import settings

def handle(exam_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     query = '''
          SELECT q.*, eq.order_num
          FROM TBL_questions q
          JOIN TBL_exam_questions eq ON eq.question_id = q.id
          WHERE eq.exam_id = ?
          ORDER BY eq.order_num
     '''
     cursor.execute(query, (exam_id,))
     rows = cursor.fetchall()
     results = []
     for row in rows:
          q = dict(row)
          conn2 = sqlite3.connect(str(settings.DB_PATH))
          conn2.row_factory = sqlite3.Row
          cursor2 = conn2.cursor()
          query2 = '''
               SELECT id, answer_text, is_correct
               FROM TBL_answers
               WHERE question_id = ?
               ORDER BY id ASC
          '''
          cursor2.execute(query2, (q['id'],))
          answers = cursor2.fetchall()
          conn2.close()
          q['answers'] = [dict(a) for a in answers]
          results.append(q)
     conn.close()
     return results