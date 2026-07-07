# controllers/report_stats.py
import sqlite3
import settings

def handle(exam_id):
     dbc = sqlite3.connect(settings.DB_PATH)
     cursor = dbc.cursor()
     cursor.execute('''
          SELECT COUNT(*) FROM exam_participants
          WHERE exam_id = ? AND is_finished = 1
     ''', (exam_id,))
     total = cursor.fetchone()[0]
     if total == 0:
          dbc.close()
          return {'total_participants': 0, 'average_score': 0, 'highest_score': 0, 'lowest_score': 0, 'difficult_questions': []}
     cursor.execute('''
          SELECT AVG(score), MAX(score), MIN(score)
          FROM exam_participants
          WHERE exam_id = ? AND is_finished = 1
     ''', (exam_id,))
     avg, high, low = cursor.fetchone()
     cursor.execute('''
          SELECT q.id, q.question_text,
                    SUM(CASE WHEN ea.is_correct = 0 THEN 1 ELSE 0 END) as wrong_count,
                    COUNT(ea.id) as total_answers
          FROM exam_answers ea
          JOIN questions q ON q.id = ea.question_id
          JOIN exam_participants ep ON ep.id = ea.participant_id
          WHERE ep.exam_id = ? AND ep.is_finished = 1
          GROUP BY q.id
          ORDER BY wrong_count DESC
          LIMIT 5
     ''', (exam_id,))
     diff = cursor.fetchall()
     dbc.close()
     return {
          'total_participants': total,
          'average_score': round(avg or 0, 2),
          'highest_score': round(high or 0, 2),
          'lowest_score': round(low or 0, 2),
          'difficult_questions': [{'id': d[0], 'text': d[1], 'wrong': d[2], 'total': d[3]} for d in diff]
     }