from Repository.FastAPIApp import FastAPIApp
from Repository.SQLiteConnection import SQLiteConnection


if __name__ == "__main__":
    sqlite = SQLiteConnection('Database/banking.db')
    app = FastAPIApp(sqlite)
    app.run()
