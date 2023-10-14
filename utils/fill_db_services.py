import sqlite3

conn = sqlite3.connect("../Database/banking.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_subcategories (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES service_categories (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bank_services (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        description TEXT,
        average_processing_time INTEGER,
        is_online BOOL
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

subcategories_data = [
    ("Кредит наличными", "", 1),
    ("Экспресс кредит", "", 1),
    ("Рефинансирование кредитов", "", 1),

    ("Платежный стикер", "", 2),
    ("Заработная плата", "", 2),
    ("Кредитная карта возможностей", "", 2),
    ("Дебетовая карта для жизни", "", 2),
    ("Детская карта", "", 2),
    ("Премиум карта Привилегия Mir Supreme", "", 2),

    ("Льготные программы", "", 3),
    ("Для семей с детьми", "", 3),
    ("Рефинансирование", "", 3),
    ("Свой дом", "", 3),
    ("Под залог имеющейся недвижимости", "", 3),
    ("Для военных", "", 3),

    ("Накопительный счет «Сейф»", "", 4),
    ("ВТБ-Вклад в рублях", "", 4),
    ("ВТБ-Вклад в юанях", "", 4),
    ("Накопительный счет «Копилка»", "", 4),
    ("Вклад «Новое время»", "", 4),
    ("Вклад «Выгодное начало»", "", 4),

    ("Счет в плюсе", "", 5),
    ("ОФЗ", "", 5),
    ("Облигации", "", 5),
    ("Акции", "", 5),
    ("Доверительное управление", "", 5),
    ("Фонды", "", 5),

    ("Антиклещ", "", 6),
    ("ОСАГО с кешбэком 10%", "", 6),
    ("КАСКО Лайт", "", 6),
    ("Спортзащита", "", 6),
    ("Страхование жилья", "", 6),
    ("Юридическая помощь", "", 6),
]

cursor.executemany('INSERT INTO service_subcategories (name, description, category_id) VALUES (?, ?, ?)',
                   subcategories_data)

conn.commit()
conn.close()
