from dataclasses import dataclass


@dataclass
class Reservation:
    id: int
    office_id: int
    reservation_date: str
    reservation_time: str
    service_id: int
    phone_number: str
    notify: bool
