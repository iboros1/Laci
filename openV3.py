from urllib.request import urlopen
from Config import PAGE_TO_OPEN, NR_OF_PAGES_TO_OPEN, SEARCH_FOR_CLASS_ID, DB
import httplib2
from bs4 import BeautifulSoup
import sqlite3
import urllib3


### ALL WARNINGS ARE DISABLED
urllib3.disable_warnings()



NR_OF_PAGES_TO_OPEN = NR_OF_PAGES_TO_OPEN
http = httplib2.Http()


def get_db_bike_list():
    connect_to_db = sqlite3.connect(DB)
    db_cusor = connect_to_db.cursor()
    db_cusor.execute('SELECT HtmlBike FROM Page')
    db_list = db_cusor.fetchall()
    connect_to_db.close()
    return db_list

db_list = get_db_bike_list()


def brows_pages():
    http = urllib3.PoolManager()
    response = http.request('GET', PAGE_TO_OPEN + '&page=' + str(page))
    return response



for page in range(NR_OF_PAGES_TO_OPEN):
    page = page
    brows_pages()

response = brows_pages()


def beautify():
    soup = BeautifulSoup(response, 'html.parser')
    soup.prettify()
    attr = {'class': [SEARCH_FOR_CLASS_ID]}
    beautiful_page_result = soup.find_all('a', attr)

