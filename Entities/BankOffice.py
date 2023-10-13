class BankOffice:
    def __init__(self, name, distance, load_factor, service_time, facilities, rating):
        self.name = name
        self.distance = distance
        self.load_factor = load_factor
        self.service_time = service_time
        self.facilities = facilities
        self.rating = rating

    def __repr__(self):
        return f'BankOffice(name="{self.name}", distance={self.distance}, load_factor={self.load_factor}, ' \
               f'service_time={self.service_time}, facilities="{self.facilities}", rating={self.rating})'

