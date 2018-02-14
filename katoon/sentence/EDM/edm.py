# -*- coding: utf-8 -*- #
import json
import random
import re

import os
import socket
import time
import urllib
import urllib2
from constant import *
from bs4 import BeautifulSoup
import redis


socket.setdefaulttimeout(10)
DB = redis.Redis(host='47.94.251.202', port=6379,db=10,password='wscjxky')

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
def get_user_likesongs(user_id):
    # 用户喜欢的歌单下的所有歌
    data=requestUrl('http://music.163.com/api/user/playlist/?offset=&limit=1&uid='+str(user_id))
    res = json.loads(data)
    playlist = res['playlist'][0]
    print playlist['name']
    url = 'http://music.163.com/playlist?id=' + str(playlist['id'])
    data = (requestUrl(url))
    soup = BeautifulSoup(data, 'html.parser')
    tag_ul = soup.find('ul', class_="f-hide")
    try:
        for li in tag_ul:
            for l in li:
                song_id = l.get('href')[9:]
                playlist_name = 'user:' + str(user_id) + ':like_songs'
                DB.sadd(playlist_name, song_id)
    except Exception, e:
        print e

def get_indexpage_playlist(data):
    soup = BeautifulSoup(data, 'html.parser')
    tag_divs = soup.find_all('div', class_="u-cover u-cover-1")

    try:
        for tag_div in tag_divs:
            tag_a=tag_div.find('a')
            playlist_id = tag_a.get('href')[13:]
            DB.sadd('playlist', playlist_id)
    except Exception, e:
        print e
def get_playlist_playlistandfollower(playlist_id):
    data=requestUrl('http://music.163.com/playlist?id=' + str(playlist_id))
    soup = BeautifulSoup(data, 'html.parser')
    tag_divs = soup.find_all('a', class_="sname f-fs1 s-fc0")

    get_playlist_followuser(playlist_id)
    try:
        for tag_div in tag_divs:
            playlist_id = tag_div.get('href')[13:]
            DB.sadd('playlist', playlist_id)
    except Exception, e:
        print e
def requestUrl(url, restart=0):
    global STOP_FLAG
    # proxy={'http': 'http://39.134.93.13:80'}
    # proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    filename = url[FILE_OFFSET:]
    try:
        if  restart:
            if DB.get(filename):
                return DB.get(filename)
            else:
                # print url
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
    except urllib2.HTTPError, e:
        if hasattr(e, 'code'):
            if (e.code == 503):
                STOP_FLAG=True

    except Exception, e:
        print e

def get_playlist_followuser(playlist_id):
    # 获取歌单的追随者
    data=requestUrl('http://music.163.com/playlist?id=' + str(playlist_id))
    soup = BeautifulSoup(data, 'html.parser')
    tag_ul = soup.find('ul', class_="m-piclist f-cb")
    for li in tag_ul:
        tag_a = li.find('a')
        if tag_a != -1:
            user_id = tag_a.get('href')[14:]
            DB.sadd('users', str(user_id))

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
        print name.text
        DB.hmset('user:' + str(user_id), dic)

    except Exception, e:
        print e
def del_cache():
    keys = DB.keys()
    for i in keys:
        r = re.search(r'^\d+.+', i)
        if r:
            DB.delete(r.group(0))


def check_user_page(user_id):
    data = requestUrl('http://music.163.com/user/home?id=' + str(user_id))
    soup = BeautifulSoup(data, 'html.parser')
    tag_d = soup.find('div', class_="n-for404")
    if tag_d:
        print 'none'

if __name__ == '__main__':
    # 279254081
    # while True:
    #     playlist_idlist=[]
    #     for i in range(50):
    #         playlist_idlist.append()
    #     startthread(get_playlist_playlist(playlist_idlist),playlist_idlist)

    #多线程取user
    diedai=30
    # while True:
    #     if diedai>0:
    #         playlist_idlist = []
    #         for i in range(100):
    #             pop = DB.spop('playlist')
    #             if (DB.sadd('ori_playlist', pop)):
    #                 playlist_idlist.append(pop)
    #         time.sleep(TIME_SLEEP)
    #         startthread(get_playlist_playlistandfollower,playlist_idlist)
    #         diedai-=1
    #     else:
    #         break
    # 多线程取user_info
    STOP_FLAG=False
    # while True:
    #     if diedai > 0 and not STOP_FLAG:
    #         users_idlist = []
    #         for i in range(200):
    #             pop = DB.spop('users')
    #             if (DB.sadd('ori_users', pop)):
    #                 users_idlist.append(pop)
    #         time.sleep(TIME_SLEEP)
    #         startthread(get_user_info, users_idlist)
    #         diedai -= 1
    #     else:
    #         break


    #取用户喜欢的歌
    while True:
        if diedai > 0 and not STOP_FLAG:
            users_idlist = []
            for i in range(200):
                pop = DB.spop('users')
                users_idlist.append(pop)
            time.sleep(TIME_SLEEP)
            startthread(get_user_likesongs, users_idlist)
            diedai -= 1
        else:
            break


    # print DB.sismember('users','')
    # 取热门歌单
    # url='http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='
    # for i in range(0,701,35):
    #     get_indexpage_playlist(requestUrl(url+str(i)))
