#!/usr/bin/python3.5

from Config import PAGE_TO_OPEN, NR_OF_PAGES_TO_OPEN, SEARCH_FOR_CLASS_ID, DB, DELETE_IF_OLDER_THEN
from bs4 import BeautifulSoup
import sqlite3
import urllib3
from time import strftime
import datetime
import re

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
    bike_html = [x[0] for x in compare_lists]
    title_with_special_characters = [x[1] for x in compare_lists]
    simple_title = []
    for title in title_with_special_characters:
        if re.match("^[a-zA-Z0-9_]*$", title):
            simple_title.append(title)
        else:
            title = re.sub(r'[^\w]', ' ', title)
            simple_title.append(title)
    for single_html, single_title in zip(bike_html, simple_title):
        try:
            db_cusor.execute(
                "INSERT INTO Page (DateAdded, HtmlBike, AdName) VALUES ('%s','%s', '%s')" % (
            db_add_date, single_html, single_title))
            create_html(db_add_date, single_html, single_title)
        except sqlite3.IntegrityError:
            add_posible_duppl(db_add_date, single_html, single_title)

    connect_to_db.commit()
    db_cusor.close()


def create_html(db_add_date, single_html, single_title):
    doc = (open('results.html', 'a'))
    html_result = str(db_add_date + '<a href=' + single_html + '>' + single_title + '</a><br>' +  "\n")
    doc.write(html_result)
    doc.close()


def add_posible_duppl(db_add_date, single_html, single_title):
    doc = (open('results.html', 'a'))
    doc.write("These are possible duplicate elements" + '<br><br>' + "\n")
    html_result = str(
        db_add_date + 'Possible Duplicate ---' + '<a href=' + single_html + '>' + single_title + '</a><br>' + "\n")
    doc.write(html_result)
    doc.close()


def delete_from_db():
    t_date = datetime.datetime.now() - datetime.timedelta(days=DELETE_IF_OLDER_THEN)
    selected_date = '%s-%02d-%02d' % (t_date.year, t_date.month, t_date.day)
    connect_to_db = sqlite3.connect(DB)
    db_cusor = connect_to_db.cursor()
    db_cusor.execute("DELETE FROM Page WHERE DateAdded <= '%s' " % selected_date)
    connect_to_db.commit()
    db_cusor.close()

if __name__ == "__main__":
    # get_all_lists()
    db_bike_list = get_db_bike_list()
    web_bike_list = get_web_bikes()
    write_to_db(compare_lists(db_bike_list, web_bike_list))
    delete_from_db()
