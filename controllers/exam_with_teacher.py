# controllers/exam_with_teacher.py
import sqlite3
import settings

def handle():
     """نمایش لیست آزمون‌ها همراه با نام استاد (با JOIN)"""
     if not settings.DB_PATH.exists():
          return []

     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     try:
          query = '''
               SELECT 
                    e.id,
                    e.title,
                    e.description,
                    e.exam_date,
                    e.start_time,
                    e.duration_min,
                    e.total_score,
                    e.status,
                    u.fullname as teacher_name,
                    u.email as teacher_email
               FROM TBL_exams e
               INNER JOIN TBL_users u ON e.created_by = u.id
               ORDER BY e.created_at DESC
          '''
          cursor.execute(query)
          
          exams = [dict(row) for row in cursor.fetchall()]
          return exams

     except Exception as e:
          print("خطا در JOIN:", e)
          return []
     finally:
          conn.close()