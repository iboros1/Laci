import sqlite3
from flask import Flask
from config import DB
import os.path
from flask import jsonify, render_template




app = Flask(__name__)


#find out what this does
wsgi_app = app.wsgi_app


def open_db():
    #os.chdir("..")
    connect_to_db = sqlite3.connect(DB)
    db_cursor = connect_to_db.cursor()
    db_cursor.execute('SELECT * FROM Page')
    db_list = db_cursor.fetchall()
    bike = []
    for dit in db_list:
        bike.append(dit)
    date = [x[0] for x in bike]
    html = [x[1] for x in bike]
    title = [x[2] for x in bike]

    return date, html, title


@app.route('/')
def test_json():
    date, html, title = open_db()
    return jsonify('results.html', DateAdded=date, HtmlBike=html, AdName=title)



@app.route('/olx')
def print_items():
    #os.chdir("..")
    connect_to_db = sqlite3.connect(DB)
    db_cursor = connect_to_db.cursor()
    db_cursor.execute('SELECT * FROM Page')
    return render_template('results.html', items=db_cursor.fetchall())



open_db()

