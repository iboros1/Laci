import webbrowser
import urllib.request
import

log = open('testfile.html', 'w')

#open = webbrowser.open_new("https://www.olx.ro/hobby-sport-turism/biciclete-fitness/biciclete/?search%5Border%5D=created_at%3Adesc")

page = urllib.request.urlopen('https://www.olx.ro/hobby-sport-turism/biciclete-fitness/biciclete/?search%5Border%5D=created_at%3Adesc')
info = urllib.request.parse_http_list(str(page))
html = page.geturl()
resp = page.getcode()
print(info)
print(html)

log.write(html + '\n')
log.write(str(resp) + '\n')
log.close()
