# debug_db.py
import sqlite3
import settings

def debug():
    db = settings.DB_PATH
    print(f"📂 دیتابیس: {db}")
    if not db.exists():
        print("❌ فایل دیتابیس وجود ندارد!")
        return
    
    conn = sqlite3.connect(str(db))
    cursor = conn.cursor()
    
    # بررسی ساختار جدول exams
    cursor.execute("PRAGMA table_info(TBL_exams)")
    columns = cursor.fetchall()
    print("📋 ستون‌های جدول TBL_exams:")
    for col in columns:
        print(f"   {col[1]} ({col[2]})")
    
    # تعداد رکوردها
    cursor.execute("SELECT COUNT(*) FROM TBL_exams")
    count = cursor.fetchone()[0]
    print(f"📊 تعداد آزمون‌ها: {count}")
    
    if count > 0:
        cursor.execute("SELECT * FROM TBL_exams")
        rows = cursor.fetchall()
        for row in rows:
            print(f"   {row}")
    
    conn.close()

if __name__ == "__main__":
    debug()