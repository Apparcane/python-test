from asyncio.tasks import sleep
import requests
from bs4 import BeautifulSoup as BS
import asyncio

url = 'https://warframe.com'


async def trying():
    i = 1
    print('Starting test: ')
    while True:
        r = requests.get(url)
        print(str(i) + ') ' + str(r))
        i = i + 1
        await asyncio.sleep(2)


asyncio.run(trying())
