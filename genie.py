import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=Y',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
musics = []
for tr in trs:
     rank = tr.select_one('td.number').text[0:2].strip()
     title = tr.select_one('td.info > a.title.ellipsis').text.strip()
     album = tr.select_one('td.info > a.albumtitle.ellipsis').text.strip()
     artist = tr.select_one('td.info > a.artist.ellipsis').text.strip()
     musics.append({ 'rank': rank, 'title': title, 'album': album, 'artist': artist })

connection = MongoClient('mongodb://localhost:27017')
database = connection['recent-anthem']
collection = database['top']
result = collection.insert_many(musics)