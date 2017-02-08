import sqlite3
from flask import Flask
from config import DB
import os.path




app = Flask(__name__)


#find out what this does
wsgi_app = app.wsgi_app


@app.route('/')
def open_db():
    #os.chdir("..")
    connect_to_db = sqlite3.connect(DB)
    db_cursor = connect_to_db.cursor()
    db_cursor.execute('SELECT HtmlBike FROM Page')
    db_list = db_cursor.fetchall()
    do = []
    for dit in db_list:
        do.append(dit)
    return do
    connect_to_db.close()
    return db_list





open_db()

