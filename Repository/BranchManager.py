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
