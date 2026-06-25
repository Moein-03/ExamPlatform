import sqlite3
import os

def handle():
     if not settings.DB_PATH.exists():
          print(f"فایل دیتابیس در مسیر {settings.DB_PATH} یافت نشد. ابتدا db_setup.py را اجرا کنید.")
          return

     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()

     try:
          # درج در جدول آزمون
          exam_data = (
               'آزمون ریاضی پیشرفته', 
               'شامل مباحث توابع و حد',
               '2025-06-20',
               '10:00',
               90,
               25,
               100.0,
               'ریاضی',
               'فعال',
               'random',
               1,
               1,
          )
          
          sql = '''
               INSERT INTO TBL_exams (
                    title, description, exam_date, start_time,
                    duration_min, question_count, total_score,
                    category, status, question_selection_type,
                    allow_download, detailed_feedback
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          '''
          cursor.execute(sql, exam_data)
          conn.commit()
          print("آزمون جدید با موفقیت درج شد.")

     except Exception as e:
          print(f"خطا: {e}")
          
     finally:
          conn.close()

if __name__ == '__main__':
     handle()