#!/usr/bin/python3.5

from urllib.request import urlopen
from Config import PAGE_TO_OPEN, NR_OF_PAGES_TO_OPEN, SEARCH_FOR_CLASS_ID, DB
import httplib2
from bs4 import BeautifulSoup
import sqlite3
import urllib3


### ALL WARNINGS ARE DISABLED
urllib3.disable_warnings()

http = httplib2.Http()


def get_db_bike_list():
    connect_to_db = sqlite3.connect(DB)
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('SELECT HtmlBike FROM Page')
    db_list = db_cusor.fetchall()
    connect_to_db.close()
    return [x[0] for x in db_list]


def brows_pages(page):
    http = urllib3.PoolManager()
    response = http.request('GET', PAGE_TO_OPEN + '&page=' + str(page))
    soup = BeautifulSoup(response.data, 'html.parser')
    soup.prettify()
    attr = {'class': [SEARCH_FOR_CLASS_ID]}
    beautiful_page_result = soup.find_all('a', attr)
    return beautiful_page_result


def compare_lists(db_bike_list, web_bike_list):

    for bike in web_bike_list:
        if bike in db_bike_list:
            pass
        else:
            pass


def get_all_lists():
    db_bike_list = get_db_bike_list()
    for page in range(NR_OF_PAGES_TO_OPEN):
        web_bike_list = brows_pages(page)
        compare_lists(db_bike_list, web_bike_list)




if __name__ == "__main__":
    get_all_lists()
