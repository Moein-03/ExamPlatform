# controllers/exam_add.py
import sqlite3
import settings

def handle(data):
     if not settings.DB_PATH.exists():
          return "دیتابیس یافت نشد. ابتدا python db_setup.py را اجرا کنید."

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()

     try:
          title = data.get('title', [''])[0].strip()
          description = data.get('description', [''])[0].strip()
          exam_date = data.get('exam_date', [''])[0].strip()
          start_time = data.get('start_time', [''])[0].strip()
          duration_min = int(data.get('duration_min', ['90'])[0])
          question_count = int(data.get('question_count', ['20'])[0])
          total_score = float(data.get('total_score', ['100'])[0])
          category = data.get('category', [''])[0].strip()
          question_selection_type = data.get('question_selection_type', ['manual'])[0]
          allow_download = 1 if data.get('allow_download', ['0'])[0] == 'on' else 0
          detailed_feedback = 1 if data.get('detailed_feedback', ['1'])[0] == 'on' else 0
          created_by = int(data.get('created_by', ['1'])[0])

          if not title or not exam_date or not start_time:
               return "عنوان، تاریخ و زمان شروع الزامی است."

          sql = '''
               INSERT INTO TBL_exams (
                    title, description, exam_date, start_time, duration_min,
                    question_count, total_score, category, status,
                    question_selection_type, allow_download, detailed_feedback, created_by
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          '''
          cursor.execute(sql, (
               title, description, exam_date, start_time, duration_min,
               question_count, total_score, category, 'فعال',
               question_selection_type, allow_download, detailed_feedback, created_by
          ))

          conn.commit()
          return "آزمون با موفقیت ایجاد شد."

     except Exception as e:
          return f"خطا در ایجاد آزمون: {str(e)}"
     finally:
          conn.close()