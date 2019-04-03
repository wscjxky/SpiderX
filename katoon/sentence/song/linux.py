# -*- coding: utf-8 -*- #
from nosql import DB
import os
import socket
import time
import urllib2
from constant import *
from bs4 import BeautifulSoup
socket.setdefaulttimeout(20)
def requestUrl(url):
    print url
    time.sleep(TIME_SLEEP)
    req=urllib2.Request(url,headers=Headers)
    data = urllib2.urlopen(req).read()
    return data

def getSrc(num):
    for i in range(1,num):
        url=SOURCE_URL+'/geci/'+str(i)+'.htm'
        try:
            data = requestUrl(url)
            soup = BeautifulSoup(data, 'html.parser')
            tag_src = soup.find('div', class_="geciInfo")
            src=tag_src.text
            if (src!=''):
                tag_info=soup.find('div', class_="geciText").find_all('li')
                song_name = tag_info[0].text[4:]
                singer = tag_info[1].text[4:]
                DB.hset(singer,song_name,src)
                print song_name

        except urllib2.HTTPError, e:
            print e
            if hasattr(e, 'code'):
                if (e.code == 404):
                    continue
                elif (e.code == 502):
                    # 更换IP再试一次
                    continue
                    # return会导致回到现在来
                elif (e.code == 403):
                    continue
        except urllib2.URLError, e:
            print e
            continue
        except Exception, e:
            print e
            continue


getSrc(2)
