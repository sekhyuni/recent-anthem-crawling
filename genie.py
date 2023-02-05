import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

import datetime
 
now = datetime.datetime.now()
now_yymmdd = now.strftime('%Y%m%d')
now_hour = now.strftime('%H')

music_list = []
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=' + now_yymmdd + '&hh=' + now_hour + '&rtm=Y&pg=1', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for tr in trs:
     rank = tr.select_one('td.number').text[0:3].strip()
     title = tr.select_one('td.info > a.title.ellipsis').text.strip()
     album = tr.select_one('td.info > a.albumtitle.ellipsis').text.strip()
     artist = tr.select_one('td.info > a.artist.ellipsis').text.strip()
     music_list.append({ 'vendor': 'genie', 'rank': rank, 'title': title, 'album': album, 'artist': artist, 'crawling_time': now })
     
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=' + now_yymmdd + '&hh=' + now_hour + '&rtm=Y&pg=2', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for tr in trs:
     rank = tr.select_one('td.number').text[0:3].strip()
     title = tr.select_one('td.info > a.title.ellipsis').text.strip()
     album = tr.select_one('td.info > a.albumtitle.ellipsis').text.strip()
     artist = tr.select_one('td.info > a.artist.ellipsis').text.strip()
     music_list.append({ 'vendor': 'genie', 'rank': rank, 'title': title, 'album': album, 'artist': artist, 'crawling_time': now })
     
connection = MongoClient('mongodb://localhost:27017')
database = connection['recent-anthem']
collection = database['top.100.musics']
result = collection.insert_many(music_list)