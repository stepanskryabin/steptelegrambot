# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search goods in textile-club.ru

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
          }

SITE_URL = 'https://textile-club.ru/search/?'


def tk_parser(url: str, search: str, headers: dict) -> None:
    session = HTMLSession()
    request = session.get('https://textile-club.ru/search/?q=Штаны+0207')
    print(request.status_code)
    if request.status_code == 200:
        request.html.render(timeout=20.0)
        a = request.html.find('.element-name')
        b = a[0].find('a')
        print(b[0].links)
        print(b[0].text)
    else:
        pass


tk_parser(SITE_URL, 'Штаны 0207', HEADERS)
