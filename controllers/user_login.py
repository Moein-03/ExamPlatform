# controllers/user_login.py
import sqlite3
import settings
import hashlib

def hash_password(password):
     return hashlib.sha256(password.encode()).hexdigest()

def handle(data):
     username = data.get('username', [''])[0].strip()
     password = data.get('password', [''])[0].strip()
     
     print(f"تلاش برای لاگین با username: {username}, password: {password}")
     
     if not username or not password:
          print("فیلدهای خالی")
          return None
     
     conn = sqlite3.connect(str(settings.DB_PATH))
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()

     hashed_password = hash_password(password)
     cursor.execute('''
          SELECT * FROM TBL_users
          WHERE email = ? AND password = ?
     ''', (username, hashed_password))
     
     row = cursor.fetchone()
     conn.close()
     
     if row:
          user = dict(row)
          print(f"کاربر پیدا شد: {user['email']}")
          return user
     else:
          print(f"کاربری با ایمیل {username} و رمز وارد شده یافت نشد.")
          return None