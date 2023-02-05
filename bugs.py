import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

import datetime
 
now = datetime.datetime.now()

music_list = []
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://music.bugs.co.kr/chart', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#container > section > div.innerContainer > div#CHARTrealtime > table.byChart > tbody > tr')
for tr in trs:
     rank = tr.select_one('td > div.ranking > strong').text.strip()
     title = tr.select_one('th > p.title > a').text.strip()
     album = tr.select_one('td > a.album').text.strip()
     artist = tr.select_one('td > p.artist > a').text.strip()
     music_list.append({ 'vendor': 'bugs', 'rank': rank, 'title': title, 'album': album, 'artist': artist, 'crawling_time': now })

connection = MongoClient('mongodb://localhost:27017')
database = connection['recent-anthem']
collection = database['top.100']
result = collection.insert_many(music_list)