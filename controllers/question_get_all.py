# controllers/question_get_all.py
import sqlite3
import settings
import json

def handle(teacher_id=None):
     dbc = sqlite3.connect(settings.DB_PATH)
     dbc.row_factory = sqlite3.Row
     cursor = dbc.cursor()
     if teacher_id:
          cursor.execute('SELECT * FROM questions WHERE teacher_id = ? ORDER BY created_at DESC', (teacher_id,))
     else:
          cursor.execute('SELECT * FROM questions ORDER BY created_at DESC')
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