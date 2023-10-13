import sqlite3


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
        select_query = "SELECT * FROM bank_offices WHERE longitude BETWEEN ? AND ? AND latitude BETWEEN ? AND ?"
        self.cursor.execute(select_query, (longitude_min, longitude_max, latitude_min, latitude_max))
        rows = self.cursor.fetchall()
        offices = []
        for row in rows:
            office = {
                "id": row[0],
                "latitude": row[-6],
                "longitude": row[-5],
            }
            offices.append(office)
        return offices

    def close(self):
        self.conn.close()

