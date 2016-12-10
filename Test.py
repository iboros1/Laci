import webbrowser
from bs4 import BeautifulSoup
import httplib2
import urllib3


http = httplib2.Http()

#log = open('testfile.html', 'w')

#open = webbrowser.open_new("https://www.olx.ro/hobby-sport-turism/biciclete-fitness/biciclete/?search%5Border%5D=created_at%3Adesc")


url = 'www.upwork.com/ab/account-security/login'

status, response = http.request('http://www.upwork.com/ab/account-security/login')
soup = BeautifulSoup(response, 'html.parser')
soup.prettify()


http = urllib3.PoolManager()
headers = urllib3.util.make_headers(basic_auth='')
r = http.request('GET', url, headers=headers)
r2 = BeautifulSoup(r, 'html.parser')
print(r2)
attr = {'class': ['job-title-link']}

#print(soup)
for link in soup.find_all('a', attr):
    job = link.get('href')
    #print(job)


