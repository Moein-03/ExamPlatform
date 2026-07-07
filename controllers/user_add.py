# controllers/user_add.py
import sqlite3
import settings

def handle(data):
    try:
        firstname = data.get('firstname', [''])[0].strip()
        lastname = data.get('lastname', [''])[0].strip()
        username = data.get('username', [''])[0].strip()
        password = data.get('password', [''])[0].strip()
        if not all([firstname, lastname, username, password]):
            return "همه فیلدها الزامی هستند"
        dbc = sqlite3.connect(settings.DB_PATH)
        cursor = dbc.cursor()
        cursor.execute('''
            INSERT INTO users (firstname, lastname, username, password, role)
            VALUES (?, ?, ?, ?, 0)
        ''', (firstname, lastname, username, password))
        dbc.commit()
        dbc.close()
        return "ثبت نام با موفقیت انجام شد"
    except sqlite3.IntegrityError:
        return "نام کاربری قبلاً ثبت شده است"
    except Exception as e:
        return f"خطا: {e}"