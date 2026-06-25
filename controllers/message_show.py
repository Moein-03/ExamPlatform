import sqlite3
from pathlib import Path
import settings

def handle():
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_name, user_email, user_message, subject, created_at FROM TBL_messages ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    results = [dict(row) for row in rows]
    return results