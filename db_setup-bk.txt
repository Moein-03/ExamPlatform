# db_setup.py
import sqlite3
import os
import settings

def setup_database():
    # اگر دیتابیس وجود دارد، حذفش کن تا از نو ساخته شود
    if os.path.exists(settings.DB_PATH):
        print(f"[!] دیتابیس {settings.DB_NAME} از قبل وجود دارد. حذف می‌شود...")
        os.remove(settings.DB_PATH)

    print(f"[*] ساخت دیتابیس جدید: {settings.DB_NAME}")
    dbc = sqlite3.connect(settings.DB_PATH)
    cursor = dbc.cursor()

    # جدول users
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role INTEGER DEFAULT 0,
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول sessions
    cursor.execute('''
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # جدول questions
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL CHECK (question_type IN ('multiple_choice', 'fill_blank')),
            options TEXT,
            correct_answer TEXT NOT NULL,
            difficulty INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id)
        )
    ''')

    # جدول exams
    cursor.execute('''
        CREATE TABLE exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            duration INTEGER NOT NULL,
            total_questions INTEGER DEFAULT 0,
            is_random INTEGER DEFAULT 0,
            is_published INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id)
        )
    ''')

    # جدول exam_questions
    cursor.execute('''
        CREATE TABLE exam_questions (
            exam_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            order_num INTEGER DEFAULT 0,
            PRIMARY KEY (exam_id, question_id),
            FOREIGN KEY (exam_id) REFERENCES exams(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # جدول exam_participants
    cursor.execute('''
        CREATE TABLE exam_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            submitted_at TIMESTAMP,
            score REAL DEFAULT 0,
            is_finished INTEGER DEFAULT 0,
            FOREIGN KEY (exam_id) REFERENCES exams(id),
            FOREIGN KEY (student_id) REFERENCES users(id),
            UNIQUE(exam_id, student_id)
        )
    ''')

    # جدول exam_answers
    cursor.execute('''
        CREATE TABLE exam_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT,
            is_correct INTEGER DEFAULT 0,
            FOREIGN KEY (participant_id) REFERENCES exam_participants(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            UNIQUE(participant_id, question_id)
        )
    ''')

    # جدول exam_reports (اختیاری)
    cursor.execute('''
        CREATE TABLE exam_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            total_participants INTEGER DEFAULT 0,
            average_score REAL DEFAULT 0,
            highest_score REAL DEFAULT 0,
            lowest_score REAL DEFAULT 0,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        )
    ''')

    # ایجاد کاربر ادمین پیش‌فرض
    cursor.execute('''
        INSERT INTO users (firstname, lastname, username, password, role)
        VALUES ('Admin', 'System', 'admin', 'admin123', 2)
    ''')

    dbc.commit()
    dbc.close()
    print("[+] دیتابیس با موفقیت ساخته شد.")
    print("[+] کاربر ادمین پیش‌فرض: username='admin', password='admin123'")

if __name__ == '__main__':
    setup_database()