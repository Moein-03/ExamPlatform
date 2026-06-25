import sqlite3
import os
import settings

def setup_database():
    if not os.path.exists(settings.DB_NAME):

        print(f"[*] ساخت دیتابیس: {settings.DB_NAME}")
        conn = sqlite3.connect(settings.DB_NAME)
        cursor = conn.cursor()

        # جدول کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TBL_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('student', 'teacher')) NOT NULL,
                university_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # جدول پیام‌های تماس با ما
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TBL_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                user_message TEXT,
                subject TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # جدول آزمون‌ها (جایگزین products)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TBL_exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                exam_date DATE NOT NULL,
                start_time TIME NOT NULL,
                duration_min INTEGER NOT NULL,
                question_count INTEGER NOT NULL,
                total_score REAL NOT NULL,
                category TEXT,
                status TEXT DEFAULT 'پیش‌نویس',
                question_selection_type TEXT DEFAULT 'manual',   -- manual / random
                allow_download BOOLEAN DEFAULT 0,
                detailed_feedback BOOLEAN DEFAULT 1,
                created_by INTEGER,    -- آی دی استاد از جدول users
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()
        print("[+] دیتابیس و جداول users, messages, exams با موفقیت ساخته شد.")

    else:
        print(f"[!] دیتابیس {settings.DB_NAME} از قبل وجود دارد.")

if __name__ == '__main__':
    setup_database()