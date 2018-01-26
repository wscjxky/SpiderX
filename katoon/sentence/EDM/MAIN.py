# -*- coding: utf-8 -*- #
import base64
import json

import re
import requests

from nosql import DB
import os
import socket
import time
import urllib
import urllib2
from constant import *
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
import plotly.plotly as py
import plotly.graph_objs as go


def requestByFixfox(url, restart=0):
    filename = url[FILE_OFFSET:]
    if not restart:
        return DB.get(filename)
    else:

        # time.sleep(TIME_SLEEP)
        options = Options()
        # options.add_argument('-headless')
        # driver = Firefox(executable_path='C:\Python27\geckodriver.exe', firefox_options=options)
        driver = Chrome(executable_path='chromedriver.exe')

        driver.get(url)

        wait = WebDriverWait(driver, timeout=5)
        if (driver.execute_script("return document.readyState")) == "complete":
            # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'iptarea' )))

            data = driver.page_source
            driver.quit()
    return data


def requestUrl(url, restart=0):
    filename = url[FILE_OFFSET:]
    try:
        if not restart:
            if DB.get(filename):
                return DB.get(filename)
            else:
                print url
                time.sleep(TIME_SLEEP)
                req = urllib2.Request(url, headers=M_Headers)
                data = urllib2.urlopen(req).read()
                DB.set(filename, data)
                return data
        else:
            print url
            time.sleep(TIME_SLEEP)
            req = urllib2.Request(url, headers=M_Headers)
            data = urllib2.urlopen(req).read()
            # DB.set(filename, data)
            return data
    except Exception, e:
        print e


def postUrl(url, keywords, restart=0):
    filename = url[FILE_OFFSET:]
    if not restart:
        return DB.get(filename)
    else:
        data = {
            's': keywords,
            'offset': 0,
            'limit': 30,
            'type': 1000,
        }
        data = requests.post(url, data).text
        DB.set(filename, data)
    return data


def getUserIdList(data):
    soup = BeautifulSoup(data, 'html.parser')
    tag_ul = soup.find('ul', class_="f-hide")
    try:
        for li in tag_ul:
            for l in li:
                song_id = l.get('href')[9:]
                song_name = l.text
                playlist_name = 'playlist:' + + ":" + song_id
                DB.hset(playlist_name, 'song_id', song_id)
                DB.hset(playlist_name, 'song_name', song_name)
    except Exception, e:
        print e


def get_user_playlists(user_id, data):
    # 去掉playcount==0
    res = json.loads(data)
    play_id_list = []
    try:
        for playlist in res['playlist']:
            playlist_playcount = playlist['playCount']
            if not playlist_playcount == '0':
                playlist_id = playlist['id']
                playlist_name = 'user:' + str(user_id) + ':playlist:' + str(playlist_id)
                DB.hset(playlist_name, 'playlist_id', playlist_id)
                DB.hset(playlist_name, 'playlist_name', playlist['name'])
                DB.hset(playlist_name, 'playlist_playcount', playlist_playcount)
                DB.hset(playlist_name, 'user_id', user_id)
                if playlist_id:
                    play_id_list.append(playlist_id)
    except Exception, e:
        print e
    return play_id_list


def get_playlist_song(playlist_id, data):
    # 获取歌单内的歌
    soup = BeautifulSoup(data, 'html.parser')
    tag_ul = soup.find('ul', class_="f-hide")
    try:
        for li in tag_ul:
            for l in li:
                song_id = l.get('href')[9:]
                song_name = l.text
                playlist_name = 'playlist:' + str(playlist_id)
                DB.hset(playlist_name, 'song_id', song_id)
                DB.hset(playlist_name, 'song_name', song_name)
    except Exception, e:
        print e
        # if (src != ''):
        #     tag_info = soup.find('div', class_="geciText").find_all('li')
        #     song_name = tag_info[0].text[4:]
        #     singer = tag_info[1].text[4:]
        #     DB.hset(singer, song_name, src)
        #     print song_name


def get_playlist_id():
    play_id_list = []
    keys = DB.keys()
    for key in keys:
        if 'playlist' in key:
            play_id_list.append(key[9:])
            print key[9:]
    return play_id_list
    # print(requestUrl('http://music.163.com/playlist?id=264257752'))


def search():
    pass


# data=(requestUrl('http://music.163.com/discover/playlist/?order=hot&cat=%E6%AC%A7%E7%BE%8E'))
def get_user_allsongs():
    data = requestUrl('http://music.163.com/api/user/playlist/?offset=&limit=100&uid=264257752')
    playlist_id_list = get_user_playlists(264257752, data)
    for play_id in playlist_id_list:
        url = 'http://music.163.com/playlist?id=' + play_id
        play_source = (requestUrl(url))
        print play_source
        # get_playlist_song(play_id,play_source)


def get_user_likesongs(user_id, data):
    # 用户喜欢的歌单下的所有歌
    res = json.loads(data)
    for playlist in res['playlist']:
        if '喜欢' in playlist['name'].encode('utf8'):
            print playlist['name']
            url = 'http://music.163.com/playlist?id=' + str(playlist['id'])
            data = (requestUrl(url))
            soup = BeautifulSoup(data, 'html.parser')
            tag_ul = soup.find('ul', class_="f-hide")
            try:
                for li in tag_ul:
                    for l in li:
                        song_id = l.get('href')[9:]
                        playlist_name = 'user:' + str(user_id) + ':like_song'
                        DB.rpush(playlist_name, song_id)
            except Exception, e:
                print e
        break


def get_user_top():
    user_id = 264257752
    with open(TEMP_FILE, 'r') as f:
        j = json.loads(f.read())
        arr = j['weekData'] + j['allData']
        for song in arr:
            song_score = song['score']
            song_id = song['song']['id']
            song_name = song['song']['name']
            print song_name
            DB.rpush('user:' + str(user_id) + ':top_song', song_id)


def get_song_playlist(data):
    # 获取包含该歌曲的歌单
    link = []
    soup = BeautifulSoup(data, 'html.parser')
    s = soup.find('ul', class_='m-rctlist f-cb')
    tag_a = s.find_all('a', attrs={"data-res-action": "log"})
    for a in tag_a:
        playlist_id = a.get('data-res-id')
        link.append(playlist_id)
    link = set(link)
    return link




def get_playlist_like(playlist, data):
    soup = BeautifulSoup(data, 'html.parser')
    tag_ul = soup.find('ul', class_="m-piclist")
    print tag_ul

    try:
        for li in tag_ul:
            for l in li:
                user_id = l.get('data-res-id')
                user_name = l.get('title')
                DB.hset('playlist:' + str(playlist) + ':like_user_id:' + str(user_id), 'user_id', user_id)
    except Exception, e:
        print e


def get_song_info(song_id):
    url = 'http://music.163.com/api/song/detail/?id=' + str(song_id) + '&ids=%5B' + str(song_id) + '%5D'
    res = requestUrl(url)
    try:
        data = json.loads(res)
        song_info = data['songs'][0]
        dic = {}
        print song_info['name']
        dic['name'] = song_info['name']
        dic['id'] = song_info['id']
        dic['position'] = song_info['position']
        dic['artist'] = song_info['artists'][0]['name']
        dic['score'] = song_info['score']
        dic['popularity'] = song_info['popularity']
        DB.hmset('songs:' + str(song_id), dic)
    except Exception, e:
        print e


def get_song_lyric(song_id):
    url = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(song_id) + '&lv=-1&kv=-1&tv=-1'
    res = requestUrl(url)
    try:
        data = json.loads(res)
        song_info = data['songs'][0]
        dic = {}
        dic['name'] = song_info['name']
        dic['id'] = song_info['id']
        dic['position'] = song_info['position']
        dic['artist'] = song_info['artists'][0]['name']
        dic['score'] = song_info['score']
        dic['popularity'] = song_info['popularity']
        DB.hmset('songs:' + str(song_id), dic)
    except Exception, e:
        print e


def get_user_info(user_id):
    url = 'http://music.163.com/user/home?id=' + str(user_id)
    data = requestUrl(url)
    try:
        soup = BeautifulSoup(data, 'html.parser')
        dic = {}
        city= soup.find('div', attrs={'class': 'inf'}).find('span')
        name = soup.find('span', attrs={'class': 'tit f-ff2 s-fc0 f-thide'})
        if name:
            dic['name']=name.text
        if city:
            dic['city']=city.text[5:]
        dic['img'] = soup.find('dt', attrs={'id': 'ava'}).find('img').get('src')

        DB.hmset('user:' + str(user_id), dic)

    except Exception, e:
        print e


def get_relation_user(ori_user):
    users_list = DB.lrange('user', 0, 26)
    top_songs = DB.lrange('user:' + str(ori_user) + ':top_song', 0, 250)
    for top in top_songs:
        for user in users_list:
            hname = 'combine:' + str(user)
            tname = 'user:' + str(user) + ':like_song'
            songs = DB.lrange(tname, 0, 500)
            for s in songs:
                if top == s:
                    print top
                    DB.rpush(hname, str(s))


def del_cache():
    keys = DB.keys()
    for i in keys:
        r = re.search(r'^\d+.+', i)
        if r:
            DB.delete(r.group(0))


# song_id=445546970
keywords = '殻ノ少女'


# res= postUrl('http://music.163.com/api/search/pc',keywords)
# res=json.loads(res)
# 获取这首个包含的歌单下喜欢这个歌单的人

def get_song_playlist_likeuser(songid):
    res = requestUrl('http://music.163.com/song?id=' + str(songid))
    for play_id in get_song_playlist(res):
        data = requestUrl('http://music.163.com/playlist?id=' + str(play_id))
        users_list = get_playlist_followuser(data)
        # users_list=DB.lrange('user',0,26)
        for user_id in users_list:
            data = requestUrl('http://music.163.com/api/user/playlist/?offset=&limit=5&uid=' + str(user_id))
            get_user_likesongs(user_id, data)

        # 获取用户喜欢
        # for i in keys:
        #     if 'top_song' in i:
        #         print i[24:]
        #         DB.rpush('she_song',i[24:])

        # top_songs=DB.lrange('user:264257752:top_song',0,300)
        # for top_id in top_songs:
        #     print top_id

        # for i in keys:
        #     res=re.findall(r'user:(\d*$)', i, )
        # user = re.findall(r'user:(\d*):like_song', i)
        # song = re.findall(r'like_song:(\d*$)', i)
        # if(res):
        # DB.rpush(p+':like_song',song[0])
        # DB.delete(i)


def get_alluser_id():
    return DB.lrange('user', 0, 100)


# 获取这首歌包含的歌单下喜欢这个歌单的人
# songid=123
# get_song_playlist_likeuser(songid)

a = 'playlist:12312312'
b = 'playlist:112997474:like_song'
c = '123123'
del_cache()


import threading
class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func
    def run(self):
        apply(self.func, self.args)  # apply就把run里的参数args传入fun中---url
def startthread(fucname, urllist, ):
    threadlist=[]
    for i in urllist:
        threadlist.append(MyThread(fucname, (i,)))
    for t in threadlist:
        t.setDaemon(True)  # 如果你在for循环里用，不行， 因为上一个多线程还没结束又开始下一个
        t.start()
    for j in threadlist:
        j.join()
def ewmysleep(i):
    print i
    time.sleep(1)
if __name__ == '__main__':
    id = 264257752
    a = [432271872, 492496544, 551951796]
    # for i in a:
    #     get_user_info(i)
    # for i in range(10606,10634,300):
    #     urlList=DB.lrange('ori_songs',i,i+300)
    #     startthread(get_song_info,urlList)
    #     print i
    #     print 'ok'
    #     del_cache()
    #     time.sleep(5)

# user_list=get_alluser_id()
# for user in user_list:
#     get_user_info(user)


















# keys=DB.keys()
# for i in keys:
#     song_id=re.findall(r'playlist:\d+:(\d+$)',i)
#     # playlist=re.findall(r'(playlist:\d+:\d+)$',i)
#     # print playlist[0]
#     if song_id:
#         DB.sadd('songs',song_id[0])
#         print song_id[0]

# get_sing_info(song_id)

# data=requestByFixfox('http://music.163.com/song?id='+ str(song_id) )
# data=requestUrl('ht tp://music.163.com/playlist?id=2050704516')
# print data
# get_like_user(data)
