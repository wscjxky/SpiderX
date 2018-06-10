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
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'no-cache',
'Connection':"keep-alive",
    'Origin':'http://mnh.scu.edu.cn',
    'Host':'mnh.scu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    , 'Referer': 'http://mnh.scu.edu.cn/search_st.aspx?cate_id=22177&code=4'

}
socket.setdefaulttimeout(10)
DB = redis.Redis(host='47.94.251.202', port=6379, db=2, password='wscjxky')
key_cache = 'cache:'
re_chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
base_url = 'http://mnh.scu.edu.cn'
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

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
def requestByFixfox(url,keyname):
    keyname = 'scu:'
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', firefox_options=options)
    wait = WebDriverWait(driver, timeout=5)
    driver.get(url)
    wait.until(expected.visibility_of_element_located((By.TAG_NAME, 'img')))
    for i in range(55):
        # try:
        #     keyname = 'scu:'
        # except:
        #     pass
        # if DB.get(keyname):
        #     return DB.get(keyname)
        data=driver.page_source
        page=driver.find_element_by_xpath('//*[@id="ListView1_DataPager1"]/span').text
        DB.set(keyname+page,data)
        driver.find_element_by_xpath('//*[@id="ListView1_DataPager1"]/input[3]').click()
        # page=driver.find_element_by_xpath('//*[@id="ListView1_DataPager1"]/span').text
        # # wait.until(expected.visibility_of_element_located((By.TAG_NAME, 'img')))
        # data=driver.page_source
        # DB.set(keyname+page,data)
        print i
    driver.quit()
def getViewUrl(data):
    keys=DB.keys('scu:*')
    for key in keys:
        data=DB.get(key)
        soup = BeautifulSoup(data, 'html.parser')
        tags_div = soup.find_all('div', class_="content_block")
        for tag_div in tags_div:
            tag_a=tag_div.find('a')
            href= base_url+tag_a.get('href')[1:]
            sort_name=re_chinese_words.search(href).group(0)
            DB.sadd('pic_view_url:'+  sort_name,href)
def getloadPic(url,sort_name):
    # data=(requestByFixfox('http://mnh.scu.edu.cn/search_st.aspx?cate_id=22177&code=4'))
    keys=DB.keys('pic_view_url:*')
    print keys[64:]
    for k in keys[70:80]:
        mem=DB.smembers(k)
        for i in mem:
            sort_name = re_chinese_words.search(i.decode('utf8')).group(0)
            getloadPic(i,sort_name)

    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', firefox_options=options)
    try:
        wait = WebDriverWait(driver, timeout=5)
        driver.get(url)
        wait.until(expected.visibility_of_element_located((By.TAG_NAME, 'img')))
        src = driver.find_element_by_xpath('//*[@id="pic_view"]').get_attribute('src')
        DB.sadd('pic_real_url:'+sort_name,(src))
        print sort_name
        driver.close()
    except Exception as e:
        driver.close()
        print e

def downloadPic(url,key_name,index):
    key_name=key_name[13:].decode('utf8')
    # with open('newindex.txt', 'a') as f:
    #     f.write(index +dirname.encode('utf8') + '\n')
    try:
        os.mkdir('images/' + key_name)
    except Exception as e:
        print e
    request = urllib2.Request(url, headers=M_Headers)
    response = urllib2.urlopen(request)
    with open("images/%s/%s.jpg" % (key_name,index), "wb") as f:
        f.write(response.read())
    print url



if __name__ == '__main__':
    keys = DB.keys('pic_real_url:*')
    for key in keys:
        memebers=DB.smembers(key)
        for index,m in enumerate(memebers):
            print m
            downloadPic(m,key,index)

            # while True:
    #     for k in keys[num:num+5]:
    #         mem=DB.smembers(k)
    #         for i in mem:
    #             url_list.append(i)
    #             sort_name = re_chinese_words.search(i.decode('utf8')).group(0)
    #             sort_name_list.append(sort_name)
    #     startthread(getloadPic,url_list,sort_name_list)
    #     num+=5
        # downloadPic(i,sort_name,1)

    # requestUrl('http://mnh.scu.edu.cn/bb_pic_view.aspx?er_id=2631972&paramMap.name=银斑豹蛱蝶','werwer')

    # clickNext(data)

