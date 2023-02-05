from pymongo import MongoClient

import numpy
from operator import itemgetter
import datetime
 
now = datetime.datetime.now()
now_yymmdd = now.strftime('%Y%m%d')
now_hour = now.strftime('%H')

def top_common_musics_creator():
    connection = MongoClient('mongodb://localhost:27017')
    database = connection['recent-anthem']
    collection = database['top.100.musics']
    
    bugs = {}
    genie = {}
    melon = {}
    for music in collection.find({ 'crawling_time': now_yymmdd + now_hour }):
        if (music['vendor'] == 'bugs'):
            bugs[music['title']] = { 'rank': music['rank'], 'title': music['title'], 'album': music['album'], 'artist': music['artist'], 'crawling_time': music['crawling_time'] }
        elif (music['vendor'] == 'genie'):
            genie[music['title']] = { 'rank': music['rank'], 'title': music['title'], 'album': music['album'], 'artist': music['artist'], 'crawling_time': music['crawling_time'] }
        else:
            melon[music['title']] = { 'rank': music['rank'], 'title': music['title'], 'album': music['album'], 'artist': music['artist'], 'crawling_time': music['crawling_time'] }
    
    common_music_list = []
    for title, music in bugs.items():
        if (title in genie and title in melon):
            rank_list = [int(bugs[title]['rank']), int(genie[title]['rank']), int(melon[title]['rank'])]
            rank_average = numpy.mean(rank_list)
            common_music_list.append({ 'rank_average': rank_average, 'title': music['title'], 'album': music['album'], 'artist': music['artist'], 'crawling_time': music['crawling_time'] })

    sorted_common_music_list = sorted(common_music_list, key=itemgetter('rank_average'))
    for idx, music in enumerate(sorted_common_music_list):
        sorted_common_music_list[idx]['rank'] = idx + 1
    
    collection = database['top.common.musics']
    result = collection.insert_many(sorted_common_music_list)

top_common_musics_creator()
    