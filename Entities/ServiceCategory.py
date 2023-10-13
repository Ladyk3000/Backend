class ServiceCategory:
    def __init__(self, name):
        self.name = name
        self.service_list = []

    def add_service(self, service):
        self.service_list.append(service)

    def remove_service(self, service):
        if service in self.service_list:
            self.service_list.remove(service)

    def display_services(self):
        print(f"Category: {self.name}")
        for service in self.service_list:
            print(f"- {service.name}: {service.description}")
