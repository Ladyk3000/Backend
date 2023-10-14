from dataclasses import dataclass


@dataclass
class BankingService:
    id: int
    name: str
    description: str
    average_processing_time: int = 15
    is_online: bool = True
