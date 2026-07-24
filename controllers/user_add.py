# controllers/user_add.py
import sqlite3
import settings
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def handle(data):
    try:
        fullname = data.get('fullname', [''])[0].strip()
        email = data.get('email', [''])[0].strip()
        password = data.get('password', [''])[0].strip()
        role = data.get('role', ['student'])[0].strip()
        university_id = data.get('university_id', [''])[0].strip()

        if not all([fullname, email, password]):
            return "همه فیلدهای الزامی پر شوند"

        if role not in ['student', 'teacher']:
            role = 'student'

        hashed = hash_password(password)
        conn = sqlite3.connect(str(settings.DB_PATH))
        cursor = conn.cursor()
        query = '''
            INSERT INTO TBL_users (fullname, email, password, role, university_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (fullname, email, hashed, role, university_id))
        conn.commit()
        conn.close()
        return "ثبت نام با موفقیت انجام شد"
    except sqlite3.IntegrityError:
        return "این ایمیل قبلاً ثبت شده است"
    except Exception as e:
        return f"خطا: {e}"