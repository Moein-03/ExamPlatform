# controllers/question_delete.py
import sqlite3
import settings

def handle(question_id, teacher_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     cursor = dbc.cursor()
     cursor.execute('DELETE FROM questions WHERE id = ? AND teacher_id = ?', (question_id, teacher_id))
     dbc.commit()
     dbc.close()
     return "سوال حذف شد"