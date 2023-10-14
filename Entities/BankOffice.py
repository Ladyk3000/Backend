from collections import deque
from dataclasses import asdict
import numpy as np
from Entities.BankingService import BankingService


class BankOffice:
    def __init__(self, database, id_, name, post_index, address, latitude, longitude):
        self.database = database
        self.id = id_
        self.name = name
        self.post_index = post_index
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.distance = None
        self.load_rate = self.get_load_rate()
        self.rating = self.get_rating()
        self.provided_services = self.get_services()
        self.digital_queue = deque(maxlen=160)

    def get_load_rate(self):
        digital_queue_score = self.get_digital_queue_score()
        smart_cam_score = self.get_smart_cam_score()
        digital_queue_weight = 0.8
        smart_cam_weight = 0.2
        load_rate = round(float(digital_queue_weight * digital_queue_score + smart_cam_weight * smart_cam_score), 1)
        return load_rate

    @staticmethod
    def get_digital_queue_score():
        min_wait_minutes = 3
        max_wait_minutes = 10
        mean_wait_time_per_hour = float(np.random.uniform(min_wait_minutes, max_wait_minutes, 1))
        return round(mean_wait_time_per_hour / max_wait_minutes, 2)

    @staticmethod
    def get_smart_cam_score(threshold=0.8):
        capacity = 100
        people_income_per_hour = np.random.uniform(50, 150, 1)
        people_outcome_per_hour = np.random.uniform(50, 150, 1)
        current_people_inside = float(people_income_per_hour - people_outcome_per_hour)
        load_coefficient = current_people_inside / (threshold * capacity)
        return round(load_coefficient, 2)

    @staticmethod
    def get_rating():
        min_value = 35
        max_value = 50
        random_number = np.random.uniform(min_value, max_value, 1)
        random_rating = round(random_number[0] / 10, 1)
        return random_rating

    def get_services(self):
        select_query = f"SELECT id, name, description, average_processing_time, is_online FROM bank_services"
        self.database.cursor.execute(select_query)
        data = self.database.cursor.fetchall()
        return [asdict(BankingService(*row)) for row in data]

    def __repr__(self):
        return str(self.__dict__)

    def as_dict(self):
        self_d = {
            "id": self.id,
            "name": self.name,
            "post_index": self.post_index,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "distance": self.distance,
            "load_rate": self.load_rate,
            "rating": self.rating,
            "provided_services": self.provided_services
        }
        return self_d
