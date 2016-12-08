import httplib2
from bs4 import BeautifulSoup
import sqlite3
import time



## dd/mm/yyyy format
time = time.strftime("%d/%m/%Y")

conn = sqlite3.connect('olx.db')
do = conn.cursor()
http = httplib2.Http()
status, response = http.request('https://www.olx.ro/hobby-sport-turism/biciclete-fitness/biciclete/?search[order]=created_at%3Ades')


soup = BeautifulSoup(response, 'html.parser')
soup.prettify()
attr = {'class': ['marginright5']}
# Create table
# do.execute('''CREATE TABLE Page
#               (date text, Html text)''')
for link in soup.find_all('a', attr):
    bike = link.get('href').replace(';promoted', '')
    # Insert a row of data
    do.execute("INSERT INTO Page VALUES ('%s','%s')" % (time, bike))



# Save (commit) the changes
conn.commit()
conn.close()
