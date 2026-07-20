# check_db.py
import sqlite3
import settings
import hashlib

def hash_password(password):
     return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect(str(settings.DB_PATH))
cursor = conn.cursor()

cursor.execute("SELECT id, email, password, role FROM TBL_users")
rows = cursor.fetchall()

print("کاربران موجود در دیتابیس:")
for row in rows:
     print(f"ID: {row[0]}, Email: {row[1]}, Password (hash): {row[2][:20]}..., Role: {row[3]}")

# تست هش کردن admin123
test_hash = hash_password("admin123")
print(f"\nهش رمز 'admin123': {test_hash}")

conn.close()