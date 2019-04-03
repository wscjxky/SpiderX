# -*- coding: utf-8 -*- #
import os
import socket
import time
import urllib
import urllib2

from bs4 import BeautifulSoup

socket.setdefaulttimeout(15)
from sentence.sql import addData
from test import getValueip

retry_times=0
MAX_TIMES=3
TIME_SLEEP=2
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    ,'Referer': 'http://www.baidu.com/'

}
def saveFile(filename,data):
    with open(filename+'.txt','a') as f:
        f.write(data)
def requestUrl(url):
    global IP_list
    time.sleep(TIME_SLEEP)
    if len(IP_list)==0:
        return
    proxy = IP_list[0]
    print proxy
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    opener.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
    urllib2.install_opener(opener)  # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
    print url
    data = urllib2.urlopen(url).read()
    return data
def getDynlinks(url):
    links = []
    if os.path.exists('Dynlinks.txt'):
        with open('Dynlinks.txt') as f:
            print 'file'
            data=f.read()
    else:
        req = urllib2.Request(url, headers=Headers)
        data = urllib2.urlopen(req).read()
        saveFile('Dynlinks',data)
    soup = BeautifulSoup(data, 'html.parser')
    tag = soup.find_all('div', class_="wrlist")
    tag_a = tag[0].find_all('a')
    for link in tag_a:
        link_href = link.get('href')
        links.append(source_url+link_href)
    return links

def getWriterlinks(url,dyn_title):
    global retry_times
    if retry_times>5:
        return
    #使用的时候要decode，传递的时候要encode
    filename=('Writerlinks'+dyn_title)
    links=[]
    if os.path.exists(filename+'.txt'):
        with open(filename+'.txt','r') as f:
            print 'file'+filename
            data = f.read()
    else:
        try:
            data=requestUrl(url)
            saveFile(filename, data)
        except Exception, e:
            print e
            retry_times+=1
            getWriterlinks(url,dyn_title)
    soup = BeautifulSoup(data, 'html.parser')
    tag_all = soup.find_all('div', class_="views-field-tid")
    for tag in tag_all:
        tag_a = tag.find_all('a')
        for link in tag_a:
            link_href = link.get('href')
            links.append(source_url+link_href)
    return links

def getSenlinks(url,wrt_name,start=8,Links=''):
    global retry_times,IP_list
    if not Links:
        Links=[]
    #使用的时候要encode为unicode，传递写入文件的时候要decode
    filename=('Sentencelinks'+wrt_name)
    # if os.path.exists(filename+'.txt'):
    #     with open(filename+'.txt','r') as f:
    #         print 'file'+filename
    #         data = f.read()
    #         soup = BeautifulSoup(data, 'html.parser')
    #         tag_all = soup.find_all('a', title="查看本句")
    #         for tag in tag_all:
    #             print  tag.text
    #             sentence = tag.text
    #             links.append(sentence)
    # else:
    for i in range(start,10):
        for j in range(MAX_TIMES):
            new_url=url +'?page='+str(i)
            try:
                data=requestUrl(new_url.encode('utf8'))
                soup = BeautifulSoup(data, 'html.parser')
                tag_all = soup.find_all('a', title="查看本句")
                for tag in tag_all:
                    sentence = tag.text
                    print sentence
                    Links.append(sentence)
                break
            except urllib2.HTTPError, e:
                print e
                if hasattr(e, 'code'):
                    if (e.code == 404):
                        break
                    elif (e.code == 502):
                        # 更换IP再试一次
                        IP_list.pop(0)
                        continue
                        #return会导致回到现在来
                    elif (e.code == 403):
                        IP_list.pop(0)
                        continue
            except urllib2.URLError,e:
                print e

            except Exception, e:

                print 'try'+str(i)
    return Links



def clearstr(str):
    str=str.replace("\n", "")
    str=str.replace(' ', '')
    return str
def transUrl():
    return

if __name__ == '__main__':
    url='http://www.juzimi.com/writers'
    source_url='http://www.juzimi.com'
    # print getIplist()
    IP_list= getValueip()
    dynasty_links=getDynlinks(url)
    time.sleep(0.1)
    for dyn_link in dynasty_links:
        dyn_title=dyn_link[30:]
        #把utf8中文转换为%url字符 ,把中文的utf8转换为python能用的unicode
        print dyn_title
        dyn_link=dyn_link[:30]+urllib.quote(dyn_title.encode('utf8'))
        time.sleep(1)
        writer_links=getWriterlinks(dyn_link,dyn_title)
        for wr_link in writer_links:
            writer=urllib.unquote(wr_link[29:].encode('utf8'))
            sentences=getSenlinks(wr_link,writer.decode('utf8'))
            print sentences
            for s in sentences:
                addData(dyn_title,writer.decode('utf8'),s)
        break


