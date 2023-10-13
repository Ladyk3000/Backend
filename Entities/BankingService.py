from dataclasses import dataclass

@dataclass
class BankingService:
    name: str
    description: str
    average_processing_time: int = 15

    def display_info(self):
        print(f"Название услуги: {self.name}")
        print(f"Описание: {self.description}")
        print(f"Среднее время выполнения: {self.average_processing_time} минут")


