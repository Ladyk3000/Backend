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
        self.rating = self.get_rating()
        self.provided_services = self.get_services()

    @staticmethod
    def get_rating():
        min_value = 35
        max_value = 50
        random_number = np.random.uniform(min_value, max_value, 1)
        random_rating = round(random_number[0] / 10, 1)
        return random_rating

    def get_services(self):
        select_query = f"SELECT * FROM bank_services"
        self.database.cursor.execute(select_query)
        data = self.database.cursor.fetchall()
        return [asdict(BankingService(*row)) for row in data]
