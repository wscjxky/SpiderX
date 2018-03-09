# -*- coding: utf-8 -*- #
import re
import json
import random
import re
import os
import socket
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
import redis

TIME_SLEEP = 1
M_Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    , 'Referer': 'http://music.163.com/user/fans?id=97526496'

}
socket.setdefaulttimeout(10)
DB = redis.Redis(host='47.94.251.202', port=6379, db=2, password='wscjxky')
key_cache = 'cache:'
re_chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
baike_url = 'https://baike.baidu.com/item/'
data_file = 'data.txt'
sort_list = []

import threading


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func

    def run(self):
        apply(self.func, self.args)  # apply就把run里的参数args传入fun中---url


def startthread(fucname, url_list, sort_list):
    threadlist = []
    for i, j in zip(url_list, sort_list):
        threadlist.append(MyThread(fucname, (i, j,)))
    for t in threadlist:
        t.setDaemon(True)  # 如果你在for循环里用，不行， 因为上一个多线程还没结束又开始下一个
        t.start()
    for j in threadlist:
        j.join()


def requestUrl(url, sort, restart=True):
    global STOP_FLAG
    # proxy={'http': 'http://39.134.93.13:80'}
    # proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    filename = key_cache + sort
    try:
        if restart:
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
            DB.set(filename, data)
            return data
    except urllib2.HTTPError, e:
        if hasattr(e, 'code'):
            if (e.code == 503):
                STOP_FLAG = True


def getUrlData():
    url_list = []
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for l in lines:
            sort_list.append(re_chinese_words.search(l.decode('utf8')).group(0))
    for sort in sort_list:
        url_list.append((baike_url + sort).encode('utf-8'))
    startthread(requestUrl, url_list, sort_list)


def getPicData():
    keys = DB.keys('cache:*')
    url_list = []
    sort_list = []
    for key in keys:
        try:
            data = DB.get(key)
            sort = key[6:]
            pic_url = (re.search(u"(/pic/.+)/0", data)).group(1)
            album_url = 'https://baike.baidu.com' + pic_url
            url_list.append(album_url)
            sort_list.append(sort+':pic')
            print 'pic:'+sort
        except Exception as e:
            print e
    startthread(requestUrl, url_list, sort_list)
def getPicUrl():
    key_pic='pic:'
    keys = DB.keys('cache:*:pic')
    for key in keys:
        data=DB.get(key)
        new_key= key[6:]
        print key
        pic= re.findall(u'img  src="(.*?)"',data)
        for i in pic:
            DB.sadd(key_pic + new_key[:-4], i)
        pic= re.findall(u'img src="(.*?)"', data)
        for j in pic:
            DB.sadd(key_pic + new_key[:-4], j)


keys = DB.keys('pic:*')
for key in keys:
    data=DB.smembers(key)
    try:
        os.mkdir(key[4:].decode('utf-8'))
        for index,i in enumerate(data):
            request = urllib2.Request(i, None, M_Headers)
            response = urllib2.urlopen(request)
            with open("%s/%s.jpg" % (key[4:].decode('utf-8'),str(index)), "wb") as f:
                f.write(response.read())
            print(i)
    except:
        pass
