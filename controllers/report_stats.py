# controllers/report_stats.py
import sqlite3
import settings

def handle(exam_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()
     
     # تعداد شرکت‌کنندگان
     cursor.execute('''
          SELECT COUNT(*) FROM TBL_exam_users
          WHERE exam_id = ? AND status = 'completed'
     ''', (exam_id,))
     total = cursor.fetchone()[0]
     
     if total == 0:
          conn.close()
          return {
               'total_participants': 0,
               'avg_score': 0,
               'max_score': 0,
               'min_score': 0,
               'difficult_questions': []
          }
     
     # آمار نمرات
     cursor.execute('''
          SELECT AVG(score), MAX(score), MIN(score)
          FROM TBL_exam_users
          WHERE exam_id = ? AND status = 'completed'
     ''', (exam_id,))
     avg, high, low = cursor.fetchone()
     
     # سوالات دشوار (برای نمایش در آینده)
     # فعلاً خالی برمی‌گردانیم چون جدول پاسخ‌های دقیق نداریم
     conn.close()
     
     return {
          'total_participants': total,
          'avg_score': round(avg or 0, 2),
          'max_score': round(high or 0, 2),
          'min_score': round(low or 0, 2),
          'difficult_questions': []
     }