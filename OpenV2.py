#!/usr/bin/python

from urllib.request import urlopen
from Config import PAGE_TO_OPEN, NR_OF_PAGES_TO_OPEN, SEARCH_FOR_CLASS_ID
import httplib2
from bs4 import BeautifulSoup
import sqlite3
import time


http = httplib2.Http()

db_list = []


def unused_open_page():
    http = urlopen(PAGE_TO_OPEN)
    olx = http.geturl()
    # print(olx)
    return olx


def get_web_bike_list(beautiful_page_result):
    web_list = []
    db_add_date = time.strftime("%Y-%m-%d")
    for bike_list in beautiful_page_result:
        bike_url = bike_list.get('href')
        bike_url, diez, unused_id = bike_url.partition('#')
        title = bike_list.find_all('strong')
        temp_bike_list = [db_add_date, bike_url, title]
        web_list.append(temp_bike_list)
    return web_list


def brows_pages():
    for page in range(NR_OF_PAGES_TO_OPEN):
        status, response = http.request(PAGE_TO_OPEN + '&page=' + str(page))
        soup = BeautifulSoup(response, 'html.parser')
        soup.prettify()
        attr = {'class': [SEARCH_FOR_CLASS_ID]}
        beautiful_page_result = soup.find_all('a', attr)
        get_web_bike_list(beautiful_page_result)



def get_db_bike_list():
    connect_to_db = sqlite3.connect('olx.db')
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('SELECT HtmlBike FROM Page')
    db_list = db_cusor.fetchall()
    connect_to_db.close()
    return db_list


def compare_web_and_db():
    filter_web_list = [x[1] for x in web_list]
    for item in filter_web_list:
        if item  in db_list:
            print(item)


compare_web_and_db()

def add_new_bike_to_db():
    pass


def write_to_db(db_cursor):
    db_add_date = time.strftime("%Y-%m-%d")
#    db_cursor.execute(
#        "INSERT INTO Page (DateAdded, HtmlBike, AdName) VALUES ('%s','%s', '%s')" % (db_add_date, bike_url, title))


def work_in_db():
    db_add_date = time.strftime("%Y-%m-%d")
    connect_to_db = sqlite3.connect('olx.db')
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('SELECT HtmlBike FROM Page')
    db_bike_html = db_cusor.fetchall()
    bike_list = [x[0] for x in db_bike_html]

    if bike_list not in bike_list:
        write_to_db(db_cusor)
    else:
        print("a")

    connect_to_db.commit()
    connect_to_db.close()

work_in_db()



