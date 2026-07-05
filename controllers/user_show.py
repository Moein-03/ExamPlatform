# controllers/user_show.py
import sqlite3
import settings

def handle():
    if not settings.DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, fullname, email, role, university_id, created_at FROM TBL_users ORDER BY id DESC")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        return result
    except Exception as e:
        print(f"Error in user_show: {e}")
        return []
    finally:
        conn.close()