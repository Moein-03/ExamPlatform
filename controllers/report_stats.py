# controllers/report_stats.py
import sqlite3
import settings

def handle(exam_id):
     conn = sqlite3.connect(str(settings.DB_PATH))
     cursor = conn.cursor()

     query = '''
          SELECT COUNT(*) FROM TBL_exam_users
          WHERE exam_id = ? AND status = 'completed'
     '''
     cursor.execute(query, (exam_id,))
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
     query = '''
          SELECT AVG(score), MAX(score), MIN(score)
          FROM TBL_exam_users
          WHERE exam_id = ? AND status = 'completed'
     '''
     cursor.execute(query, (exam_id,))
     avg, high, low = cursor.fetchone()
     
     conn.close()
     
     return {
          'total_participants': total,
          'avg_score': round(avg or 0, 2),
          'max_score': round(high or 0, 2),
          'min_score': round(low or 0, 2),
          'difficult_questions': []
     }