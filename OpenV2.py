#!/usr/bin/python

from urllib.request import urlopen
from Config import page_to_open, page_nr

page_nr = page_nr


def open_page(http):
    http = urlopen(page_to_open)
    olx = http.geturl()
    print(http)
    return http, olx

http = open_page(http)

def brows_pages(http, page_nr):
    for page_nr in range(page_nr):
        status, response = http.request(page_to_open + '&page=' + str(page_nr))
        print(response)

brows_pages(http, page_nr)