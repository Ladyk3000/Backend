import sqlite3
import json

with open('../Data/atms.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)['atms']

conn = sqlite3.connect("../Database/banking.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bank_atms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        latitude REAL,
        longitude REAL,
        allDay BOOLEAN,
        wheelchair_service TEXT,
        blind_service TEXT,
        nfcForBankCards_service TEXT,
        qrRead_service TEXT,
        supportsUsd_service TEXT,
        supportsChargeRub_service TEXT,
        supportsEur_service TEXT,
        supportsRub_service TEXT
    )
''')


for atm in data:
    cursor.execute('''
        INSERT INTO bank_atms (address, latitude, longitude, allDay, wheelchair_service, blind_service, nfcForBankCards_service, qrRead_service, supportsUsd_service, supportsChargeRub_service, supportsEur_service, supportsRub_service)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        atm['address'],
        atm['latitude'],
        atm['longitude'],
        atm['allDay'],
        atm['services']['wheelchair']['serviceCapability'],
        atm['services']['blind']['serviceCapability'],
        atm['services']['nfcForBankCards']['serviceCapability'],
        atm['services']['qrRead']['serviceCapability'],
        atm['services']['supportsUsd']['serviceCapability'],
        atm['services']['supportsChargeRub']['serviceCapability'],
        atm['services']['supportsEur']['serviceCapability'],
        atm['services']['supportsRub']['serviceCapability']
    ))

conn.commit()
conn.close()
