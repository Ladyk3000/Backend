import sqlite3
import json

with open('../Data/offices.txt', 'r', encoding='utf-8') as file:
    data = file.read()

offices_data = json.loads(data)

conn = sqlite3.connect("../Database/banking.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bank_offices (
        id INTEGER PRIMARY KEY,
        salePointName TEXT,
        post_index TEXT,
        address TEXT,
        Monday_Thursday_schedule TEXT,
        Friday_schedule TEXT,
        Saturday_schedule TEXT,
        Sunday_schedule TEXT,
        is_rko BOOL,
        officeType TEXT,
        salePointFormat TEXT,
        suoAvailability BOOL,
        hasRamp BOOL,
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
    address = ' '.join(branch_data["address"].split(',')[1:])
    post_index = branch_data["address"].split(',')[0]
    is_rko = True if branch_data["rko"] == 'есть РКО' else False
    try:
        monday_schedule = branch_data['openHours'][0]['hours']
        friday_schedule = branch_data['openHours'][-3]['hours']
        saturday_schedule = branch_data['openHours'][-2]['hours']
        sunday_schedule = branch_data['openHours'][-1]['hours']
    except IndexError:
        monday_schedule = friday_schedule = saturday_schedule = sunday_schedule = branch_data['openHours'][0]['days']
    suo_availability = True if branch_data["suoAvailability"] == 'Y' else False
    has_ramp = True if branch_data["hasRamp"] == 'Y' else False
    kep_value = int(branch_data["kep"]) if branch_data["kep"] is not None else 0
    my_branch = int(branch_data["myBranch"])

    cursor.execute('''
        INSERT INTO bank_offices (
            salePointName, address, post_index, is_rko, 
            Monday_Thursday_schedule, Friday_schedule, Saturday_schedule, Sunday_schedule,
            officeType, salePointFormat, suoAvailability, hasRamp,
            latitude, longitude, metroStation,
             distance, kep, myBranch
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        branch_data["salePointName"], address, post_index, is_rko,
        monday_schedule, friday_schedule, saturday_schedule, sunday_schedule,
        branch_data["officeType"], branch_data["salePointFormat"], suo_availability, has_ramp,
        branch_data["latitude"], branch_data["longitude"], branch_data["metroStation"],
        branch_data["distance"], kep_value, my_branch
    ))

conn.commit()
conn.close()
