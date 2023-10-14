from Repository.BranchManager import BranchManager
from Repository.FastAPIApp import FastAPIApp
from Repository.SQLiteConnection import SQLiteConnection


if __name__ == "__main__":
    sqlite = SQLiteConnection('Database/banking.db')
    manager = BranchManager(sqlite)
    app = FastAPIApp(manager, sqlite)
    app.run()
