# controllers/user_add.py
import sqlite3
import settings
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def handle(data):
    if not settings.DB_PATH.exists():
        return "دیتابیس یافت نشد."

    conn = sqlite3.connect(str(settings.DB_PATH))
    cursor = conn.cursor()
    try:
        fullname = data.get('fullname', [''])[0].strip()
        email = data.get('email', [''])[0].strip()
        password = data.get('password', [''])[0].strip()
        role = data.get('role', ['student'])[0]
        university_id = data.get('university_id', [''])[0].strip()

        if not fullname or not email or not password:
            return "نام، ایمیل و رمز عبور الزامی است."

        hashed = hash_password(password)
        sql = '''INSERT INTO TBL_users (fullname, email, password, role, university_id) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (fullname, email, hashed, role, university_id))
        conn.commit()
        return "کاربر با موفقیت ثبت شد."
    except sqlite3.IntegrityError:
        return "این ایمیل قبلاً ثبت شده است."
    except Exception as e:
        return f"خطا: {str(e)}"
    finally:
        conn.close()