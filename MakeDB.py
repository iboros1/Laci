import sqlite3


def make_db():

    conn = sqlite3.connect('olx.db')
    do = conn.cursor()

    do.execute('''CREATE TABLE Page (AddDate date , Html text unique)''')

    conn.commit()
    conn.close()
make_db()
