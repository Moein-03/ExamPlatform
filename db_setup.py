import sqlite3
import os
import settings

def setup_database():
    if not os.path.exists(settings.DB_PATH):
        print(f"[*] ساخت دیتابیس: {settings.DB_NAME}")
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TBL_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('student', 'teacher', 'admin')) NOT NULL,
                university_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

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
                question_selection_type TEXT DEFAULT 'manual',
                allow_download BOOLEAN DEFAULT 0,
                detailed_feedback BOOLEAN DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES TBL_users(id)
            )
        ''')

        # Insert admin sample
        cursor.execute("INSERT OR IGNORE INTO TBL_users (fullname, email, password, role) VALUES ('Admin', 'admin@example.com', '1234', 'admin')")

        conn.commit()
        conn.close()
        print("[+] دیتابیس ساخته شد.")
    else:
        print("[!] دیتابیس وجود دارد.")

if __name__ == '__main__':
    setup_database()