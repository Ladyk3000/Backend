import random
import sqlite3

from Repository.PathFinder import PathFinder


class SQLiteConnection:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def get_categories(self):
        select_query = "SELECT name FROM service_categories"
        self.cursor.execute(select_query)
        category_names = [row[0] for row in self.cursor.fetchall()]
        return category_names

    def get_subcategories_by_category(self, category_id):
        select_query = f"SELECT name FROM service_subcategories WHERE category_id={category_id}"
        self.cursor.execute(select_query)
        subcategories = [row[0] for row in self.cursor.fetchall()]
        return subcategories

    def get_offices_for_maps(self, longitude_min, latitude_min, longitude_max, latitude_max):
        select_query = "SELECT id, latitude, longitude FROM bank_offices " \
                       "WHERE longitude BETWEEN ? AND ? AND latitude BETWEEN ? AND ?"
        self.cursor.execute(select_query, (longitude_min, longitude_max, latitude_min, latitude_max))
        rows = self.cursor.fetchall()
        offices = []
        for row in rows:
            office = {
                "id": row[0],
                "latitude": row[1],
                "longitude": row[2],
            }
            offices.append(office)
        return offices

    def get_atms_for_maps(self, longitude_min, latitude_min, longitude_max, latitude_max):
        select_query = "SELECT id, latitude, longitude FROM bank_atms " \
                       "WHERE longitude BETWEEN ? AND ? AND latitude BETWEEN ? AND ?"
        self.cursor.execute(select_query, (longitude_min, longitude_max, latitude_min, latitude_max))
        rows = self.cursor.fetchall()
        atms = []
        for row in rows:
            office = {
                "id": row[0],
                "latitude": row[1],
                "longitude": row[2],
            }
            atms.append(office)
        return atms

    def get_best_office(self, longitude, latitude):
        select_query = "SELECT id, longitude, latitude FROM bank_offices"
        self.cursor.execute(select_query)
        offices = self.cursor.fetchall()

        distances = []
        for office in offices:
            office_id, office_longitude, office_latitude = office
            distance = PathFinder.haversine(latitude, longitude, office_latitude, office_longitude)
            distances.append((office_id, distance))

        distances.sort(key=lambda x: x[1])
        closest_offices = distances[:5]

        best_offices = []
        for office_id, _ in closest_offices:
            self.cursor.execute("SELECT id, longitude, latitude, address  FROM bank_offices WHERE id = ?", (office_id,))
            office = self.cursor.fetchone()
            if office:
                best_offices.append({
                    "id": office[0],
                    "longitude": office[1],
                    "latitude": office[2],
                    "address": office[2],
                    "load_rate": random.randint(1, 9) * 0.1
                })

        return best_offices

    def close(self):
        self.conn.close()
