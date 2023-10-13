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

    def get_services_by_category(self, category_id):
        select_query = f"SELECT name FROM banking_services WHERE category_id={category_id}"
        self.cursor.execute(select_query)
        services = [row[0] for row in self.cursor.fetchall()]
        return services

    def close(self):
        self.conn.close()

