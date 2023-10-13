from Repository.FastAPIApp import FastAPIApp
from Repository.SQLiteConnection import SQLiteConnection


if __name__ == "__main__":
    sqlite = SQLiteConnection('Database/banking.db')
    my_app = FastAPIApp(sqlite)
    my_app.run()
