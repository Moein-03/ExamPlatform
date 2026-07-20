# db_setup.py
import sqlite3
import settings
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    conn = sqlite3.connect(str(settings.DB_PATH))
    cursor = conn.cursor()

    # حذف جداول قدیمی (اگر وجود داشته باشند)
    cursor.execute("DROP TABLE IF EXISTS TBL_users")
    cursor.execute("DROP TABLE IF EXISTS TBL_exams")
    cursor.execute("DROP TABLE IF EXISTS TBL_questions")
    cursor.execute("DROP TABLE IF EXISTS TBL_answers")
    cursor.execute("DROP TABLE IF EXISTS TBL_exam_users")
    cursor.execute("DROP TABLE IF EXISTS TBL_exam_questions")
    cursor.execute("DROP TABLE IF EXISTS TBL_messages")

    # ===== جدول کاربران =====
    cursor.execute('''
        CREATE TABLE TBL_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            university_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ===== جدول آزمون‌ها =====
    cursor.execute('''
        CREATE TABLE TBL_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT,
            duration INTEGER,
            teacher_id INTEGER,
            is_published INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES TBL_users(id) ON DELETE SET NULL
        )
    ''')

    # ===== جدول سوالات =====
    cursor.execute('''
        CREATE TABLE TBL_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            question_type TEXT DEFAULT 'single',
            score REAL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES TBL_exams(id) ON DELETE CASCADE
        )
    ''')

    # ===== جدول پاسخ‌ها (گزینه‌ها) =====
    cursor.execute('''
        CREATE TABLE TBL_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES TBL_questions(id) ON DELETE CASCADE
        )
    ''')

    # ===== جدول ثبت‌نام دانشجویان در آزمون =====
    cursor.execute('''
        CREATE TABLE TBL_exam_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            score REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES TBL_exams(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES TBL_users(id) ON DELETE CASCADE,
            UNIQUE(exam_id, user_id)
        )
    ''')

    # ===== جدول ارتباط سوالات با آزمون (در صورت نیاز) =====
    cursor.execute('''
        CREATE TABLE TBL_exam_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            order_number INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES TBL_exams(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES TBL_questions(id) ON DELETE CASCADE,
            UNIQUE(exam_id, question_id)
        )
    ''')

    # ===== جدول پیام‌ها =====
    cursor.execute('''
        CREATE TABLE TBL_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            subject TEXT,
            user_message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ===== ایجاد کاربر admin =====
    admin_email = "admin@exam.com"
    admin_password = hash_password("admin123")
    cursor.execute('''
        INSERT OR IGNORE INTO TBL_users (fullname, email, password, role, university_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("مدیر سیستم", admin_email, admin_password, "admin", "0"))

    conn.commit()
    conn.close()
    print("دیتابیس با موفقیت ساخته شد.")
    print("کاربر ادمین admin: admin@exam.com / admin123")