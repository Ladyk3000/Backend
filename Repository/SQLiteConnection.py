import datetime
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

    def get_best_office(self, longitude, latitude, k=5):
        closest_offices = self.get_nearest_branches(branch_type='office', longitude=longitude, latitude=latitude, k=k)
        best_offices = []
        for office_id, distance in closest_offices:
            self.cursor.execute("SELECT id, longitude, latitude, address  FROM bank_offices WHERE id = ?", (office_id,))
            office = self.cursor.fetchone()
            if office:
                best_offices.append({
                    "id": office[0],
                    "longitude": office[1],
                    "latitude": office[2],
                    "address": office[3],
                    "distance": distance,
                    "load_rate": self.get_load_rate()
                })

        return best_offices

    def get_best_atm(self, longitude, latitude):
        closest_atms = self.get_nearest_branches(branch_type='office', longitude=longitude, latitude=latitude)
        best_atms = []
        for atm_id, distance in closest_atms:
            self.cursor.execute("SELECT id, longitude, latitude, address  FROM bank_atms WHERE id = ?", (atm_id,))
            office = self.cursor.fetchone()
            if office:
                best_atms.append({
                    "id": office[0],
                    "longitude": office[1],
                    "latitude": office[2],
                    "address": office[3],
                    "distance": distance,
                })

        return best_atms

    def get_nearest_branches(self, branch_type, latitude, longitude, k=5):
        if branch_type == 'atm':
            table = 'bank_atms'
        else:
            table = 'bank_offices'
        select_query = f"SELECT id, longitude, latitude FROM {table}"
        self.cursor.execute(select_query)
        branches = self.cursor.fetchall()
        distances = []

        for branch in branches:
            branch_id, branch_longitude, branch_latitude = branch
            distance = PathFinder.haversine(latitude, longitude, branch_latitude, branch_longitude)
            distances.append((branch_id, distance))

        distances.sort(key=lambda x: x[1])
        closest_branches = distances[:k]
        return closest_branches

    def get_office_info(self, office_id, longitude, latitude):
        office_info = self.get_branch_info(branch_type='office', branch_id=office_id)
        distance = PathFinder.haversine(lat1=latitude,
                                        lon1=longitude,
                                        lat2=office_info['latitude'],
                                        lon2=office_info['latitude'])
        load_rate = self.get_load_rate()
        office_info['distance'] = distance
        office_info['load_rate'] = load_rate
        return office_info

    def get_branch_info(self, branch_type, branch_id):
        if branch_type == 'atm':
            table = 'bank_atms'
        else:
            table = 'bank_offices'
        self.cursor.execute(f"SELECT id, longitude, latitude, address  FROM {table} WHERE id = ?", (branch_id,))
        branch = self.cursor.fetchone()
        branch_info = None
        if branch:
            branch_info = {
                "id": branch[0],
                "longitude": branch[1],
                "latitude": branch[2],
                "address": branch[3],
            }
        if branch_type == 'office':
            branch_info['load_rate'] = self.get_load_rate()
        return branch_info

    def get_atm_info(self, atm_id, longitude, latitude):
        atm_info = self.get_branch_info(branch_type='atm', branch_id=atm_id)
        distance = PathFinder.haversine(lat1=latitude,
                                        lon1=longitude,
                                        lat2=atm_info['latitude'],
                                        lon2=atm_info['latitude'])
        atm_info['distance'] = distance
        return atm_info

    @staticmethod
    def get_load_rate():
        return random.randint(1, 9) * 0.1

    def get_reservation_days(self, office_id):
        today = datetime.date.today()

        reservation_days = []
        is_saturday_working = self.is_saturday_working(office_id)
        day_counter = 0
        while len(reservation_days) < 7:
            day_counter += 1
            next_day = today + datetime.timedelta(days=day_counter)
            if self.is_working_day(next_day, is_saturday_working):
                reservation_days.append(next_day.isoformat())
        return reservation_days

    @staticmethod
    def is_working_day(date, is_saturday_working):
        if date.weekday() == 6:
            return False
        if date.weekday() == 5 and not is_saturday_working:
            return False
        return True

    def is_saturday_working(self, office_id):
        self.cursor.execute(f"SELECT Saturday_schedule FROM bank_offices WHERE id = ?", (office_id,))
        schedule = self.cursor.fetchone()[0]
        is_saturday_working = False if schedule in ['выходной', 'Не обслуживает ЮЛ'] else True
        return is_saturday_working

    def get_time_slots(self, office_id, reservation_date):
        working_hours = self.get_working_hours(office_id, reservation_date)
        time_slots = self.generate_time_slots(working_hours)
        return time_slots

    def get_working_hours(self, office_id, reservation_date):
        reservation_date = datetime.date.fromisoformat(reservation_date)
        day_of_week = reservation_date.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[day_of_week]
        if day_name == 'Friday':
            day_schedule = 'Friday_Thursday_schedule'
        elif day_name == 'Saturday':
            day_schedule = 'Saturday_Thursday_schedule'
        else:
            day_schedule = 'Monday_Thursday_schedule'
        self.cursor.execute(f"SELECT {day_schedule} FROM bank_offices WHERE id = ?", (office_id,))
        schedule_string = self.cursor.fetchone()[0]
        start_time_string, end_time_string = schedule_string.split('-')
        start_time = datetime.time.fromisoformat(start_time_string)
        end_time = datetime.time.fromisoformat(end_time_string)
        return [start_time, end_time]

    @staticmethod
    def generate_time_slots(working_hours, service_time_minutes=15):
        time_slots = []
        current_time = datetime.datetime.now().replace(second=0, microsecond=0)
        current_time = current_time.replace(hour=working_hours[0].hour, minute=working_hours[0].minute)

        while current_time.time() < working_hours[1]:
            time_slots.append(current_time.time().strftime('%H:%M'))
            current_time += datetime.timedelta(minutes=service_time_minutes)

        return time_slots
