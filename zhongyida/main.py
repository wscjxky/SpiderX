import socket
import time
import urllib
import urllib
import requests
import re
from bs4 import BeautifulSoup
import redis
import json
import urllib.error
TIME_SLEEP = 1
import pymongo
from  pymongo import  MongoClient
# socket.setdefaulttimeout(100)
# conn = MongoClient('localhost', 27017)
# db = conn.mydb  #连接mydb数据库，没有则自动创建
M_Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'cookie': 'did=bJ1Wx1ENJe9I2PrMy1Tq5qMIDJsX7ANSHzSfLUJJNzbo0QHXYByVUgpXMph21nj3; ptc=RG1.3399952193253955840.1521189914; _ga=GA1.2.2051052520.1521189923; _gid=GA1.2.1722239954.1521189923; cookieconsent_dismissed=true; classification=institution; __gads=ID=98e059459b14698f:T=1521190107:S=ALNI_Maitk8x-a0nnYQhXXeqcD0WlOxmcA; sid=gq0OTCL1h0IYmf8s0EydB4Tv3KBzYbdhgSv4HmFMBJmUcnXvx1FF98yfv0CvL1hb6m0wX1vsGLHs4Ew90cSOKLqJuLPDoL2aUlun1e1OTfTxu8j6Vf9Dt16C0s8d8fPI; chseen=1; captui=MjQ0NzEwYjllOWMxN2I4MTgyNzkwYTA3ZGRlYzYxMDM2MjU4MDcwY2U2NzM1N2ZhZGViZjYxYmE0NTU1ODk0M19VQkpOY3hlY0J6ekJ4TVNVZ2x1OUljaU1VcmhDM1hjZkNyVmU%3D; rghfp=true; _gat_UA-58591210-1=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    , 'Referer': 'https://www.researchgate.net'

}
list_url='http://bjcsyzl.com/wap.php/product/index.shtml'
base_url='http://bjcsyzl.com'
# 1-8 120
# http://bjcsyzl.com/wap.php/product/lists/pid/1/p/2.shtml
DB = redis.Redis(host='47.94.251.202', port=6379, db=12, password='wscjxky', decode_responses=True)
key_cache = "cache:"

def requestUrl(url, sort):
    # proxy={'http': 'http://39.134.93.13:80'}
    # proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    filename = key_cache + sort
    print(filename)
    try:
        if DB.get(filename):
            return DB.get(filename)
        else:
            print(url)
            req = requests.get(url, headers=M_Headers)
            data=req.text
            DB.set(filename, data)
            return data
    except Exception as e:
        print (e, url)
def getList():
    for index in range(1,5):
        page_url = 'http://bjcsyzl.com/wap.php/product/lists/pid/120/p/'+str(index)+'.shtml'
        key=page_url[-12:-5]
        data=requestUrl(page_url,key)
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find('div', class_="wares-list")
        li=div.find_all('li')
        for i in li:
            a=i.find('a')
            url=base_url+a.get('href')
            info=a.find('img')
            title=info.get('alt')
            img_url=base_url+info.get('src')
            # print(title,url,img_url)
            print(title)
            key = url[-12:-5]
            source = requestUrl(page_url, key)
            dict_data={
                'title':title,
                'url':url,
                'img_url':img_url,
                'source':source
            }
            title=title.replace(' ','').replace(':','')
            DB.hmset('data:xinfengxitong:'+title,dict_data)

            # DB.hmset('data:dajin:'+title,dict_data)
            # DB.hmset('data:rili:'+title,dict_data)
            # DB.hmset('data:sanlingzhonggong:'+title,dict_data)

if __name__ == '__main__':
    getList()