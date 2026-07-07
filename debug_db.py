# debug_db.py
import sqlite3
import settings

def debug():
    db_path = settings.DB_PATH
    print(f"📂 دیتابیس: {db_path}")

    if not db_path.exists():
        print("❌ فایل دیتابیس وجود ندارد!")
        return

    dbc = sqlite3.connect(db_path)
    cursor = dbc.cursor()

    # لیست همه جدول‌ها
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("📋 جدول‌های موجود:")
    for table in tables:
        print(f"   - {table[0]}")

    # بررسی جدول users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("\n✅ جدول users وجود دارد")
        cursor.execute("SELECT id, firstname, lastname, username, role FROM users")
        users = cursor.fetchall()
        print(f"📊 تعداد کاربران: {len(users)}")
        for user in users:
            print(f"   {user}")
    else:
        print("\n❌ جدول users وجود ندارد!")

    dbc.close()

if __name__ == "__main__":
    debug()