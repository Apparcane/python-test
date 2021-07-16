# scraper.py
import requests
from bs4 import BeautifulSoup

page = 1

while True:
    url = 'https://animevost.am/ongoing/page/' + str(page) + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = soup.find_all('div', class_='shortstoryHead')

    if(len(names)):
        for el in names:
            h = el.find('h2')
            name = h.find('a')
            print(name.text)
    else:
        break
    page += 1
