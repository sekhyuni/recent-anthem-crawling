import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

import datetime
 
now = datetime.datetime.now()

music_list = []
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.melon.com/chart/index.htm', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#conts > div#tb_list > form > div > table > tbody > tr')
for tr in trs:
     rank = tr.select_one('span.rank').text.strip()
     title = tr.select_one('div.ellipsis.rank01 > span > a').text.strip()
     album = tr.select_one('div.ellipsis.rank03 > a').text.strip()
     artist = tr.select_one('div.ellipsis.rank02 > span > a').text.strip()
     music_list.append({ 'vendor': 'melon', 'rank': rank, 'title': title, 'album': album, 'artist': artist, 'crawling_time': now })

connection = MongoClient('mongodb://localhost:27017')
database = connection['recent-anthem']
collection = database['top.100']
result = collection.insert_many(music_list)