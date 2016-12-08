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
#Create table
#do.execute('''CREATE TABLE Page
#               (date1 text, Html1 text, date2 text, Html2 text)''')
for link in soup.find_all('a', attr):
    bike = link.get('href').replace(';promoted', '')
    # Insert a row of data
    do.execute("INSERT INTO Page (date1, Html1) VALUES ('%s','%s')" % (time, bike))

tabel1 = str(do.execute("SELECT date1 FROM Page LIMIT 1").fetchall())
tabel1 = tabel1.replace('[(\'', '').replace('\',)]', '')

print(tabel1 + time)

if tabel1 >= time:
    for link in soup.find_all('a', attr):
        bike = link.get('href').replace(';promoted', '')
        # Insert a row of data
        do.execute("UPDATE Page SET  date2=date2 WHERE 1")



# Save (commit) the changes
conn.commit()
conn.close()
#http://stackoverflow.com/questions/7640061/trying-to-check-if-value-already-in-mysql-db