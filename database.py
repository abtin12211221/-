import sqlite3

def init_db():
    conn = sqlite3.connect("arzoonjou.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            image_path TEXT,
            affiliate_link TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ دیتابیس و جدول محصولات با موفقیت ایجاد شدند!")

if __name__ == "__main__":
    init_db()