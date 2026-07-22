# controllers/answer_delete.py
import sqlite3
import settings

def handle(answer_id):
     try:
          conn = sqlite3.connect(str(settings.DB_PATH))
          cursor = conn.cursor()
          cursor.execute("DELETE FROM TBL_answers WHERE id = ?", (answer_id,))
          conn.commit()
          conn.close()
          return {"success": True}
     except Exception as e:
          return {"error": str(e)}