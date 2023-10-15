from Repository.BranchManager import BranchManager
from Repository.FastAPIApp import FastAPIApp
from Repository.ReservationNotifier import ReservationNotifier
from Repository.SQLiteConnection import SQLiteConnection


def main():
    sqlite = SQLiteConnection('Database/banking.db')
    notifier = ReservationNotifier('Database/banking.db')
    manager = BranchManager(sqlite)
    app = FastAPIApp(manager, sqlite, notifier)
    app.run()


if __name__ == "__main__":
    main()
