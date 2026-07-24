# controllers/question_get_by_exam.py
import sqlite3
import settings
import json

def handle(exam_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     cursor.execute('''
          SELECT q.*, eq.order_num
          FROM questions q
          JOIN exam_questions eq ON eq.question_id = q.id
          WHERE eq.exam_id = ?
          ORDER BY eq.order_num
     ''', (exam_id,))
     rows = cursor.fetchall()
     dbc.close()
     results = []
     for row in rows:
          item = dict(row)
          if item.get('options'):
               try:
                    item['options'] = json.loads(item['options'])
               except:
                    item['options'] = []
          results.append(item)
     return results