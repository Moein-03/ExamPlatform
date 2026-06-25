import sqlite3
from pathlib import Path
import settings

def handle():
    conn = sqlite3.connect(str(settings.DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, exam_date, start_time, duration_min, question_count, total_score, category, status, question_selection_type, allow_download, detailed_feedback, created_by, created_at FROM TBL_exams ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]