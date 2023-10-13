from Repository.FastAPIApp import FastAPIApp
from Repository.SQLiteConnection import SQLiteConnection


def main():
    sqlite = SQLiteConnection('Database/banking.db')
    app = FastAPIApp(sqlite)
    app.run()


if __name__ == "__main__":
    main()
