#!/usr/bin/python

from urllib.request import urlopen
from Config import page_to_open, page_nr


def open_page():
    http = urlopen(page_to_open)
    olx = http.geturl()
    print(olx)
def brows_pages():
    for page_to_open in range(page_to_open):

