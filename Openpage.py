#!/usr/bin/python

import httplib2
from bs4 import BeautifulSoup
import sqlite3
import datetime
from Config import page_nr, page_to_open, Days
import time


def page_run(page_nr, time=time):
    ## dd/mm/yyyy format
    time = time.strftime("%Y-%m-%d")
    # time = "2016-12-18"
    t_date = datetime.datetime.now() - datetime.timedelta(days=Days)
    t_date = str('%s-%02d-%02d' % (t_date.year, t_date.month, t_date.day))
    conn = sqlite3.connect('olx.db')
    do = conn.cursor()
    http = httplib2.Http()
    results = (open('results.html', 'a'))
    # do.execute('''CREATE TABLE Page (AddDate date , Html text unique)''')
    for page_nr in range(page_nr):
        status, response = http.request(page_to_open + '&page=' + str(page_nr))
        soup = BeautifulSoup(response, 'html.parser')
        soup.prettify()
        attr = {'class': ['marginright5']}

        for link in soup.find_all('a', attr):
            bike = link.get('href')
            html_link, sep, id_promoted = bike.partition('#')
            html_result = str('From Page' + str(page_nr) + '<a href=' + html_link + '>' + html_link + '</a><br>')
            write_to_db = ("INSERT INTO Page (AddDate, Html) VALUES ('%s','%s')" % (time, html_link))

            # do.execute('SELECT AddDate FROM Page WHERE AddDate')
            # first_cell = str(do.fetchone())
            # if first_cell < t_date:
            #  #do.execute("DELETE FROM Page WHERE AddDate='%s'" % first_cell)
            #
            #  print("f")
            #  print(first_cell)
            #  print("mydate")
            #  print(t_date)

            # Insert a row of data
            try:
                do.execute(write_to_db)
                results.write(html_result)
                print(html_result)

            except:
                print(str(page_nr) + "-Page: " + str(html_link) + '\n')

            do.execute("DELETE FROM Page WHERE AddDate >= '%s' " % t_date)

        # Save (commit) the changes
        conn.commit()
    results.close()

    conn.close()


if __name__ == "__main__":
    page_run(page_nr)
