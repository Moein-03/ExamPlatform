# controllers/exam_show.py
import sqlite3
import settings

def handle():
    if not settings.DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row  # برای دسترسی به داده به صورت دیکشنری
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, title, description, start_time, duration FROM TBL_exams ORDER BY id DESC")
        rows = cursor.fetchall()
        # تبدیل به لیست دیکشنری
        result = [dict(row) for row in rows]
        return result
    except Exception as e:
        print(f"Error in exam_show: {e}")
        return []
    finally:
        conn.close()