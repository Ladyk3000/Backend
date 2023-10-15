import sqlite3
from datetime import datetime

class ReservationNotifier:
    def __init__(self, database_path, emulate_sms=True):
        self.database_path = database_path
        self.emulate_sms = emulate_sms

    def send_daily_reservations(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            reservations = self.get_day_reservations(cursor)
            if reservations:
                for reservation in reservations:
                    reservation_id, phone_number, reservation_time = reservation
                    message = f"Добрый день это банк ВТБ, мы хотели бы напомнить о том," \
                              f" что у вас на сегодня в {reservation_time} запланировано бронирование"
                    self.send_sms(phone_number, message)

    @staticmethod
    def get_day_reservations(cursor):
        current_date = datetime.now().date()
        cursor.execute('''
            SELECT id, phone_number, reservation_time
            FROM reservations
            WHERE reservation_date = ? AND notify = 1
        ''', (str(current_date),))
        reservations = cursor.fetchall()
        return reservations

    def send_sms(self, receiver_number, message):
        if self.emulate_sms:
            print(f"Эмулированная отправка SMS на номер {receiver_number}: {message}")
