from collections import OrderedDict

from Entities.BankOffice import BankOffice
from Repository.SQLiteConnection import SQLiteConnection


class BranchManager:
    def __init__(self, database: SQLiteConnection):
        self.database = database
        self.atms = self.get_atms()
        self.offices = self.get_offices()

    def get_atms(self):
        data = self.database.get_branch_data(branch_type='atm')
        return []

    def get_offices(self):
        data = self.database.get_branch_data(branch_type='office')
        return [self.create_office(office_data) for office_data in data]

    def create_office(self, data):
        office_id, name, post_index, address, latitude, longitude = data
        bank_office = BankOffice(database=self.database,
                                 id_=office_id,
                                 name=name,
                                 post_index=post_index,
                                 address=address,
                                 latitude=latitude,
                                 longitude=longitude)
        return bank_office

    def get_available_services(self, office_id):
        office = [office for office in self.offices if office.id == office_id][0]
        return office.provided_services

    def get_best_office(self, longitude, latitude, k=5):
        closest = self.database.get_nearest_branches(
            branch_type='office',
            longitude=longitude,
            latitude=latitude,
            k=k
        )

        office_ids, distances = zip(*closest)
        closest_offices = [office for office in self.offices if office.id in office_ids]

        distance_weight = 0.55
        load_factor_weight = 0.35
        rating_weight = 0.1

        total_scores = {}

        for office, distance in zip(closest_offices, distances):
            load_factor_score = office.load_rate
            distance_score = distance / max(distances)
            rating_score = 5 / office.rating

            total_score = (
                    distance_weight * distance_score
                    + load_factor_weight * load_factor_score
                    + rating_weight * rating_score
            )

            total_scores[office.id] = total_score
            office.distance = distance

        sorted_total_scores = OrderedDict(sorted(total_scores.items(), key=lambda item: item[1]))

        result = [office.as_dict() for office in closest_offices if office.id in sorted_total_scores]

        return result

    def get_available_near_offices(self, service_id, longitude, latitude):
        max_results = 5
        suit_offices = []
        k = max_results
        while len(suit_offices) < max_results:
            offices_dicts = self.database.get_near_offices(longitude=longitude, latitude=latitude, k=k)
            for office_data in offices_dicts:
                office = next((o for o in self.offices if o.id == office_data['id']), None)

                if office and any(service['id'] == service_id for service in office.provided_services):
                    suit_offices.append(office)

            k += 1

            if k > 100:
                break

        return suit_offices[:max_results]
