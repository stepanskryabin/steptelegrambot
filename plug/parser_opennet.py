# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search news in opennet.org

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
          }

SITE_URL = 'https://www.opennet.ru/opennews/main.shtml'


def tk_parser(url: str, search: str = None, headers: dict = None) -> None:
    session = HTMLSession()
    request = session.get(url)
    print(request.status_code)
    if request.status_code == 200:
        links = request.html.find('.title2')
        texts = request.html.find('.chtext')
        for i in range(0, len(links)):
            print(links[i].absolute_links)
    else:
        return request.status_code


tk_parser(SITE_URL)
