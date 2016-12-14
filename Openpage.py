#!/usr/bin/python

import httplib2
from bs4 import BeautifulSoup
import sqlite3
import time, datetime
from Config import page_nr,page_to_open, Days



## dd/mm/yyyy format
time = time.strftime("%d/%m/%Y")
t_date = datetime.datetime.now() - datetime.timedelta(days=Days)
t_date = str('%02d/%02d/%s' % (t_date.day, t_date.month, t_date.year))
conn = sqlite3.connect('olx.db')
do = conn.cursor()
http = httplib2.Http()
results = (open('results.html', 'a'))


def page_run(page_nr):
    #do.execute('''CREATE TABLE Page (date date, Html text unique)''')
    for page_nr in range(page_nr):
        status, response = http.request(page_to_open + '&page=' + str(page_nr))
        soup = BeautifulSoup(response, 'html.parser')
        soup.prettify()
        attr = {'class': ['marginright5']}

        for link in soup.find_all('a', attr):
            bike = link.get('href')
            html_link, sep, id_promoted = bike.partition('#')
            html_result = str('From Page' + str(page_nr) + '<a href=' + html_link + '>' + html_link + '</a><br>')
            write_to_db = ("INSERT INTO Page (date, Html) VALUES ('%s','%s')" % (time, html_link))

            # Insert a row of data
            try:
                do.execute(write_to_db)
                results.write(html_result)
                print(html_result)

            except:
                print(str(page_nr) + "-Page: "+ str(html_link) + '\n')

        do.execute("DELETE FROM Page WHERE date <= '%s' " % t_date)
        # Save (commit) the changes
        conn.commit()
    results.close()
    conn.close()

if __name__ == "__main__":
    page_run(page_nr)