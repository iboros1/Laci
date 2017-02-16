import sqlite3
from config import DB, DELETE_IF_OLDER_THEN
import os.path
from flask import Flask, render_template, request


import datetime
from time import strftime

app = Flask(__name__)
app.database = DB

# find out what this does
wsgi_app = app.wsgi_app


#
# def open_db():
#     #os.chdir("..")
#     connect_to_db = sqlite3.connect(DB)
#     db_cursor = connect_to_db.cursor()
#     db_cursor.execute('SELECT * FROM Page')
#     db_list = db_cursor.fetchall()
#     bike = []
#     for dit in db_list:
#         bike.append(dit)
#     date = [x[0] for x in bike]
#     html = [x[1] for x in bike]
#     title = [x[2] for x in bike]
#
#     return date, html, title
#
#
# @app.route('/')
# def test_json():
#     date, html, title = open_db()
#     return jsonify('results.html', DateAdded=date, HtmlBike=html, AdName=title)
#
#
#
# @app.route('/lx')
# def print_items():
#     #os.chdir("..")
#     connect_to_db = sqlite3.connect(DB)
#     db_cursor = connect_to_db.cursor()
#     db_cursor.execute('SELECT * FROM Page')
#     return render_template('results.html', items=db_cursor.fetchall())


def date_list():
    keep_dates = []
    t_date = datetime.datetime.now() - datetime.timedelta(days=DELETE_IF_OLDER_THEN)
    date1 = '%s-%02d-%02d' % (t_date.year, t_date.month, t_date.day)
    date2 = strftime("%Y-%m-%d")
    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.datetime.strptime(date2, '%Y-%m-%d')
    step = datetime.timedelta(days=1)
    while start <= end:
        keep_dates.append(start.date())
        start += step
    return keep_dates


@app.route('/')
def bikes():
    # remove "#" When debugging
    # os.chdir("..")
    connect_to_db = sqlite3.connect(DB)
    db_cursor = connect_to_db.cursor()
    db_cursor = db_cursor.execute('SELECT * from Page')
    bikes_dict = [dict(Date=row[0],
                       Html=row[1],
                       Title=row[2]) for row in db_cursor.fetchall()]
    connect_to_db.close()

    return render_template('results.html', Bikes=bikes_dict)


@app.route('/olx', methods=['GET', 'POST'])
def form():
    # remove "#" When debugging
    # user_date = '2017-02-05'
    # os.chdir("..")
    if request.method == 'GET':
        return render_template('date.html')
    elif request.method == 'POST':
        user_date = request.form.get('date')
        select_list = []
        connect_to_db = sqlite3.connect(DB)
        db_cursor = connect_to_db.cursor()
        db_cursor = db_cursor.execute('SELECT * from Page')
        bikes_dict = [dict(Date=row[0],
                           Html=row[1],
                           Title=row[2]) for row in db_cursor.fetchall()]
        for select in bikes_dict:
            if select['Date'] == user_date:
                select_list.append(select)
        connect_to_db.close()
        return render_template('results.html', Bikes=select_list, user_date=user_date)


if __name__ == "__main__":
    form()
