# -*- coding: utf-8 -*-
# Autor: Stepan Skriabin - stepan.skrjabin@gmail.com
# Search goods in textile-club.ru

import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


SITE_URL = 'https://textile-club.ru/search/?'
session = HTMLSession()

#request1 = requests.get(SITE_URL, params={'q': 'Штаны 0207'})
#request2 = requests.get(SITE_URL, params={'q': 'Штаны 0208'})
request3 = session.get(SITE_URL, params={'q': 'Штаны 0207'})
request4 = session.get(SITE_URL, params={'q': 'Штаны 0208'})
#soup1 = bs(request1.text)
#soup2 = bs(request2.text)
soup3 = request3.html.find('div')
soup4 = request4.html.find('a')

print(soup3)
print()
print(soup4)
