import sqlite3

conn = sqlite3.connect("../Database/banking.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS banking_services (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES service_categories (id)
    )
''')

categories_data = [
    ("Кредиты",),
    ("Карты",),
    ("Ипотека",),
    ("Вклады и счета",),
    ("Инвестиции",),
    ("Страхование",)
]

cursor.executemany('INSERT INTO service_categories (name) VALUES (?)', categories_data)

services_data = [
    ("Кредит наличными", "", 1),
    ("Экспресс кредит", "", 1),
    ("Рефинансирование кредитов", "", 1)
]

cursor.executemany('INSERT INTO banking_services (name, description, category_id) VALUES (?, ?, ?)', services_data)

conn.commit()
conn.close()
