
import sqlite3


def create_db():
    connect_to_db = sqlite3.connect('olx.db')
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('''CREATE TABLE Page (DateAdded date, HtmlBike text unique, AdName text)''')
    connect_to_db.close()
    print("PageDB created")


if __name__ == "__main__":
    create_db()