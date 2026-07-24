# controllers/question_export.py
import json
import sqlite3
import settings
from core import response

def handle(teacher_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     query = '''
          SELECT id, question_text, question_type, options, correct_answer, difficulty
          FROM questions WHERE teacher_id = ?
     '''
     cursor.execute(query, (teacher_id,))
     rows = cursor.fetchall()
     dbc.close()
     questions = []
     for row in rows:
          item = dict(row)
          if item.get('options'):
               try:
                    item['options'] = json.loads(item['options'])
               except:
                    item['options'] = []
          questions.append(item)
     return response.serve_json(questions)