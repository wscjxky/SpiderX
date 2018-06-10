import socket
import time
import urllib
import urllib
import urllib2

import re
from bs4 import BeautifulSoup
import redis
import json

TIME_SLEEP = 1
# socket.setdefaulttimeout(100)
M_Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'cookie': 'did=bJ1Wx1ENJe9I2PrMy1Tq5qMIDJsX7ANSHzSfLUJJNzbo0QHXYByVUgpXMph21nj3; ptc=RG1.3399952193253955840.1521189914; _ga=GA1.2.2051052520.1521189923; _gid=GA1.2.1722239954.1521189923; cookieconsent_dismissed=true; classification=institution; __gads=ID=98e059459b14698f:T=1521190107:S=ALNI_Maitk8x-a0nnYQhXXeqcD0WlOxmcA; sid=gq0OTCL1h0IYmf8s0EydB4Tv3KBzYbdhgSv4HmFMBJmUcnXvx1FF98yfv0CvL1hb6m0wX1vsGLHs4Ew90cSOKLqJuLPDoL2aUlun1e1OTfTxu8j6Vf9Dt16C0s8d8fPI; chseen=1; captui=MjQ0NzEwYjllOWMxN2I4MTgyNzkwYTA3ZGRlYzYxMDM2MjU4MDcwY2U2NzM1N2ZhZGViZjYxYmE0NTU1ODk0M19VQkpOY3hlY0J6ekJ4TVNVZ2x1OUljaU1VcmhDM1hjZkNyVmU%3D; rghfp=true; _gat_UA-58591210-1=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    , 'Referer': 'https://www.researchgate.net'

}
DB = redis.Redis(host='47.94.251.202', port=6379, db=4, password='wscjxky', decode_responses=True)
key_cache = "paper:"


def getPaperLinkdata(data):
    soup = BeautifulSoup(data, 'html.parser')
    tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
    for tag_div in tags_div:
        href = (tag_div).get('href')
        name = tag_div.text
        DB.hset('paper_link', 'name', name)
        DB.hset('paper_link', 'href', href)


def getPaperAuthor(data):
    soup = BeautifulSoup(data, 'html.parser')
    tags_div = soup.find_all('li', class_="publication-author-list__item")
    for tag_div in tags_div:
        tag_a = tag_div.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
        print(tag_a.text)


def getCit(data):
    soup = BeautifulSoup(data, 'html.parser')
    is_cit = soup.find('span', class_='title-tab-interaction')
    is_cit = is_cit.text
    print is_cit
    if '0' in is_cit and 'Citations' in is_cit:
        return 0
    else:
        tags_ul = soup.find_all('ul',
                                class_="nova-e-list nova-e-list--size-m nova-e-list--type-inline nova-e-list--spacing-none nova-v-publication-item__person-list")
        tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
        for index, tag_div in enumerate(tags_div):
            href = (tag_div).get('href')
            print(href)
            tags_a = (tags_ul)[index].find_all('a')
            for tag_a in tags_a:
                print(tag_a.text)


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
            time.sleep(TIME_SLEEP)
            req = urllib2.Request(url, headers=M_Headers)
            data = urllib2.urlopen(req).read()
            DB.set(filename, data)
            return data

    except urllib2.URLError as e:
        print e, url
    except Exception as e:
        print e, url


from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import threading


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func

    def run(self):
        apply(self.func, self.args)


def startthread(fucname, url_list, sort_list):
    threadlist = []
    for i, j in zip(url_list, sort_list):
        threadlist.append(MyThread(fucname, (i, j,)))
    for t in threadlist:
        t.setDaemon(True)
        t.start()
    for j in threadlist:
        j.join()


def requestByFixfox(url, keyname):
    cache_key = 'paper:'
    options = Options()
    driver = Firefox(executable_path='geckodriver', firefox_options=options)
    wait = WebDriverWait(driver, timeout=100)

    driver.get(url)
    # wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'public-publication-details')))
    data = driver.page_source
    DB.set(cache_key + keyname, data)
    driver.quit()


def clickMore(url, keyname):
    cache_key = 'new_cit_paper:'
    options = Options()
    driver = Firefox(executable_path='geckodriver', firefox_options=options)
    # wait = WebDriverWait(driver, timeout=200)
    driver.get(url)
    # wait.until(expected.element_to_be_clickable((By.CLASS_NAME, 'nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-xs nova-c-button--color-grey nova-c-button--theme-ghost nova-c-button--width-auto')))
    span = driver.find_element_by_xpath('//*[@id="tabs-0"]/span/div/span[1]').text
    if '0' in span and 'Citations' in span:
        print keyname+'none'
        return 255
    while (True):
        try:
            button = driver.find_element_by_xpath('//*[@id="tabs-1"]/div/div/div/div/button')
            button.click()
            time.sleep(2)
        except:
            break
    data = driver.page_source
    DB.set(cache_key + keyname, data)
    driver.quit()


if __name__ == '__main__':
    # base_url='https://www.researchgate.net/'
    # url_1=base_url+'publication/258821296_An_Iterative_Pilot-Data_Aided_Estimator_for_OFDM-Based_Relay-Assisted_Systems'
    # url = 'https://www.researchgate.net/publication/264691859_A_distributed_mobility_management_scheme_in_networks_with_the_locatoridentifier_separation'
    # data=(requestUrl(url,url[-10:]))
    # url = 'https://www.researchgate.net/publication/304372135_Signal_detection_of_ambient_backscatter_system_with_differential_modulation'
    # title = re.search('\d+_(.+)', url).group(1).strip().replace('_', ' ')
    # requestByFixfox(url,title)
    # clickMore(url,title)
    data = requestUrl('http://localhost:8000/api/papers/', 'papers')
    cit_list=[15, 20, 22, 29, 33, 36, 37, 39, 40, 41, 42, 43, 45, 47, 48, 50, 51, 53, 54, 55, 57, 59, 60, 61, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73, 74, 81, 82, 83, 85, 87, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103, 105, 106, 108]
    data_j = json.loads(data)
    for p in data_j['results']:
        if p['id'] in cit_list[2:]:
            title,url= p['title'],p['url']
            title = re.search('(\d+)_', url).group(1).strip().replace('_', ' ')
            with open('paper_dir/'+title+'.txt','w') as f:
                f.close()
            print title,url
            # clickMore(url,title)
    # print data
    # getCit(data)
    # with open('detail','wb') as f:
    #     f.write(data)
    # lenth=len('https://www.researchgate.net/publication/261384805_')
    # keys = DB.keys('paper*')
    # for k in keys:
    #     # data = DB.get(k)
    #     query=k[6:]
    #     print query
    #     query=query.replace('_',' ')
    #     getCit(DB.get(k))
    # with open('txt.txt','r') as f:
    #     urls=f.readlines()
    #     url_list=[]
    #     sort_list=[]
    # for index,i in enumerate(urls[1:]):
    # print index
    # url_list.append(i)
    # sort_list.append(i[-10:])
    # requestUrl(i,i[lenth:])
    # startthread(requestUrl,url_list=url_list,sort_list=sort_list)
    # getPaperLinkdata(data)
    # getPaperAuthor(data)
