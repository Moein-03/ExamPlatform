# controllers/exam_get_all.py
import sqlite3
import settings
from datetime import datetime, timedelta

def handle(user_id=None, only_published=False, student_id=None):
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     query = '''
          SELECT e.*, u.fullname as teacher_name
          FROM TBL_exams e
          LEFT JOIN TBL_users u ON e.teacher_id = u.id
     '''
     params = []
     conditions = []

     if student_id:
          query = '''
               SELECT e.*, u.fullname as teacher_name
               FROM TBL_exams e
               LEFT JOIN TBL_users u ON e.teacher_id = u.id
               INNER JOIN TBL_exam_users eu ON e.id = eu.exam_id
               WHERE eu.user_id = ?
          '''
          params.append(student_id)
          if only_published:
               query += " AND e.is_published = 1"
     else:
          if user_id:
               conditions.append("e.teacher_id = ?")
               params.append(user_id)
          if only_published:
               conditions.append("e.is_published = 1")
          if conditions:
               query += " WHERE " + " AND ".join(conditions)

     query += " ORDER BY e.id DESC"
     cursor.execute(query, params)
     rows = cursor.fetchall()
     conn.close()

     now = datetime.now()
     for row in rows:
          exam = dict(row)
          if exam.get('is_published') == 0:
               exam['exam_status'] = 'پیش‌نویس'
               exam['status_class'] = 'status-draft'
          else:
               start_time_str = exam.get('start_time')
               if start_time_str:
                    try:
                         start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                         start_time = start_time.replace(tzinfo=None)
                         duration_minutes = exam.get('duration', 0)
                         end_time = start_time + timedelta(minutes=duration_minutes)
                         
                         if now < start_time:
                              exam['exam_status'] = 'فعال'
                              exam['status_class'] = 'status-active'
                         elif start_time <= now <= end_time:
                              exam['exam_status'] = 'در حال برگزاری'
                              exam['status_class'] = 'status-ongoing'
                         else:
                              exam['exam_status'] = 'به پایان رسیده'
                              exam['status_class'] = 'status-ended'
                    except:
                         exam['exam_status'] = 'نامشخص'
                         exam['status_class'] = 'status-unknown'
               else:
                    exam['exam_status'] = 'نامشخص'
                    exam['status_class'] = 'status-unknown'
          result.append(exam)

     return result