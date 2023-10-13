import sqlite3
import json

# Откройте файл для чтения JSON-данных
with open('Data/offices.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Разбор JSON-данных
offices_data = json.loads(data)

# Подключитесь к базе данных (если файл не существует, он будет создан)
conn = sqlite3.connect("bank_branches.db")
cursor = conn.cursor()

# Создайте таблицу для хранения данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bank_branches (
        id INTEGER PRIMARY KEY,
        salePointName TEXT,
        address TEXT,
        status TEXT,
        rko TEXT,
        officeType TEXT,
        salePointFormat TEXT,
        suoAvailability TEXT,
        hasRamp TEXT,
        latitude REAL,
        longitude REAL,
        metroStation TEXT,
        distance INTEGER,
        kep INTEGER,
        myBranch INTEGER
    )
''')
conn.commit()


for branch_data in offices_data:
    kep_value = branch_data["kep"] if branch_data["kep"] is not None else 0
    cursor.execute('''
        INSERT INTO bank_branches (
            salePointName, address, status, rko, officeType, salePointFormat, suoAvailability,
            hasRamp, latitude, longitude, metroStation, distance, kep, myBranch
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        branch_data["salePointName"],
        branch_data["address"],
        branch_data["status"],
        branch_data["rko"],
        branch_data["officeType"],
        branch_data["salePointFormat"],
        branch_data["suoAvailability"],
        branch_data["hasRamp"],
        branch_data["latitude"],
        branch_data["longitude"],
        branch_data["metroStation"],
        branch_data["distance"],
        kep_value,
        int(branch_data["myBranch"])
    ))

conn.commit()

# Закройте соединение с базой данных
conn.close()
