import sqlite3
import os

import settings

def handle():
    if not settings.DB_PATH.exists():
        print(f"فایل دیتابیس در مسیر {settings.DB_PATH} یافت نشد. ابتدا db_setup.py را اجرا کنید.")
        return

    conn = sqlite3.connect(str(settings.DB_PATH))
    cursor = conn.cursor()

    try:
        # درج در جدول کاربران
        user_data = ('رضا کریمی', 'reza.karimi@example.com', '123456', 'student', '98231001')
        
        sql = '''
            INSERT INTO TBL_users (fullname, email, password, role, university_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(sql, user_data)
        conn.commit()
        print("کاربر با موفقیت درج شد.")

    except sqlite3.IntegrityError as e:
        print(f"خطا: ایمیل تکراری یا مشکل یکپارچگی داده - {e}")

    except Exception as e:
        print(f"خطای غیرمنتظره: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    handle()