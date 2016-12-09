import httplib2
from bs4 import BeautifulSoup
import sqlite3
import time
from Config import *


## dd/mm/yyyy format
time = time.strftime("%d/%m/%Y")

conn = sqlite3.connect('olx.db')
do = conn.cursor()
http = httplib2.Http()


for page_nr in range(page_nr):
    status, response = http.request(page_to_open + '&page=' + str(page_nr))
    soup = BeautifulSoup(response, 'html.parser')
    soup.prettify()
    attr = {'class': ['marginright5']}
    #Create table
    # do.execute('''CREATE TABLE Page
    #              (date date, Html text unique)''')

    for link in soup.find_all('a', attr):
        bike = link.get('href')
        html_link, sep, id_promoted = bike.partition('#')  # .replace(';promoted', '')

        # Insert a row of data
        try: do.execute("INSERT INTO Page (date, Html) VALUES ('%s','%s')" % (time, html_link)), print(html_link)
        except:
            print(id_promoted)


    # Save (commit) the changes
    conn.commit()
conn.close()
    #http://stackoverflow.com/questions/7640061/trying-to-check-if-value-already-in-mysql-db