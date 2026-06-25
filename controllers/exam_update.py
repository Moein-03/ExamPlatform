import sqlite3
from urllib.parse import parse_qs
import settings

def handle(exam_id, body):
     params = parse_qs(body)
     title = params.get('title', [''])[0].strip()
     description = params.get('description', [''])[0].strip()
     exam_date = params.get('exam_date', [''])[0].strip()
     start_time = params.get('start_time', [''])[0].strip()
     duration_min = params.get('duration_min', ['0'])[0].strip()
     question_count = params.get('question_count', ['0'])[0].strip()
     total_score = params.get('total_score', ['0'])[0].strip()
     category = params.get('category', [''])[0].strip()
     status = params.get('status', ['پیش‌نویس'])[0].strip()

     if not title or not exam_date or not start_time:
          return "عنوان، تاریخ و زمان شروع الزامی است"

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     try:
          cursor.execute("""
               UPDATE TBL_exams SET
                    title=?, description=?, exam_date=?, start_time=?,
                    duration_min=?, question_count=?, total_score=?,
                    category=?, status=?
               WHERE id=?
          """, (title, description, exam_date, start_time,
               int(duration_min), int(question_count), float(total_score),
               category, status, exam_id))
          conn.commit()
          return f"آزمون با شناسه {exam_id} با موفقیت ویرایش شد."
     except Exception as e:
          return f"خطا در ویرایش: {e}"
     finally:
          conn.close()