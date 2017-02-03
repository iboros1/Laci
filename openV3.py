#!/usr/bin/python3.5

from urllib.request import urlopen
from Config import PAGE_TO_OPEN, NR_OF_PAGES_TO_OPEN, SEARCH_FOR_CLASS_ID, DB
import httplib2
from bs4 import BeautifulSoup
import sqlite3
import urllib3
from time import strftime

### ALL WARNINGS ARE DISABLED
urllib3.disable_warnings()

def get_web_bikes():
    results = []
    http = urllib3.PoolManager()
    for current_page in range(NR_OF_PAGES_TO_OPEN):
        response = http.request('GET', PAGE_TO_OPEN + '&page=' + str(current_page))
        soup = BeautifulSoup(response.data, 'html.parser')
        soup.prettify()
        attr = {'class': [SEARCH_FOR_CLASS_ID]}
        for beautiful_page_result in  soup.find_all('a', attr):
            dirty_bike_link = beautiful_page_result.get('href')
            bike_url, diez, unused_id = dirty_bike_link.partition('#')
            title = beautiful_page_result.find_all('strong')
            results.append((bike_url, title[0].text)) # create list with all the values
    return results


def get_db_bike_list():
    connect_to_db = sqlite3.connect(DB)
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('SELECT HtmlBike FROM Page')
    db_list = db_cusor.fetchall()
    connect_to_db.close()
    return [x[0] for x in db_list]


def compare_lists(db_bike_list, get_web_bikes):
    unique_bike_list = []
    for bike in get_web_bikes:
        if bike[0] not in db_bike_list:
            unique_bike_list.append(bike)
        else:
            pass
    return unique_bike_list


def write_to_db(compare_lists):
    connect_to_db = sqlite3.connect(DB)
    db_cusor = connect_to_db.cursor()
    db_add_date = strftime("%Y-%m-%d")
    db_cusor.execute(
        "INSERT INTO Page (DateAdded, HtmlBike, AdName) VALUES ('%s','%s', '%s')" % (
        db_add_date, compare_lists.bike_url, compare_lists.title))


if __name__ == "__main__":
    # get_all_lists()
    db_bike_list = get_db_bike_list()
    web_bike_list = get_web_bikes()
    write_to_db(compare_lists(db_bike_list, web_bike_list))