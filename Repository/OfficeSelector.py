from datetime import datetime, time

from Entities.BankOffice import BankOffice


class OfficeSelector:
    def __init__(self, bank_departments):
        self._user_priorities = {"distance": 0.6, "load_factor": 0.4, "service_time": 0.3}
        self.bank_departments = bank_departments

    def select_best_office(self, current_time):
        if not self.bank_departments:
            raise ValueError("No bank departments provided.")

        scores = []

        max_service_time = max(department.service_time for department in self.bank_departments)
        normalized_service_times = [department.service_time / max_service_time for department in self.bank_departments]

        for i, department in enumerate(self.bank_departments):
            distance_score = self._user_priorities["distance"] * department.distance
            load_factor_score = self._user_priorities["load_factor"] * (1 - department.load_factor)
            service_time_score = self._user_priorities["service_time"] * normalized_service_times[i]
            rating_score = department.rating
            time_of_day_score = 0.1 if current_time.time() in (time(9, 0), time(15, 0)) else 0

            total_score = distance_score + load_factor_score + service_time_score + rating_score + time_of_day_score
            scores.append(total_score)

        best_office = self.bank_departments[scores.index(max(scores))]
        return best_office


departments = [
    BankDepartment("Office A", 2.5, 0.3, 15, "ATM", 4.5),
    BankDepartment("Office B", 4.0, 0.6, 10, "ATM and Drive-Thru", 3.8),
    BankDepartment("Office C", 5.2, 0.2, 20, "ATM", 4.2),
    BankDepartment("Office D", 3.7, 0.8, 25, "ATM and Notary", 4.0),
]

office_selector = OfficeSelector(departments)

best_department = office_selector.select_best_office(datetime.now())
print(f"The best branch for the user is: {best_department.name}")
