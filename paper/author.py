import socket
import time
import urllib
import urllib
import urllib2

from bs4 import BeautifulSoup
import redis
import json

TIME_SLEEP = 1
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


def getPaperLinkdata(sort, data):

    soup = BeautifulSoup(data, 'html.parser')
    tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
    for tag_div in tags_div:
        href = (tag_div).get('href')
        name = tag_div.text
        print name



def getPaperAuthor(data,sort):
    authors=[]
    soup = BeautifulSoup(data, 'html.parser')
    # tags_div = soup.find_all('li', class_="publication-author-list__item")
    tags_div = soup.find_all('meta', property="citation_author")
    for tag_div in tags_div:
        # tag_a = tag_div.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
        authors.append(tag_div.get('content'))
    DB.hset('cit_link:' + sort, sort,json.dumps(authors))


def getCit(data,sort):
    authors=[]
    soup = BeautifulSoup(data, 'html.parser')
    tags_ul = soup.find_all('ul',
                            class_="nova-e-list nova-e-list--size-m nova-e-list--type-inline nova-e-list--spacing-none nova-v-publication-item__person-list")

    tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
    for index, tag_div in enumerate(tags_div):
        href = (tag_div).get('href')
        print(href)
        tags_a = (tags_ul)[index].find_all('a')
        for tag_a in tags_a:
            authors.append((tag_a.text).strip())
        DB.hset('cit_link:' + sort, href,json.dumps(authors))


if __name__ == '__main__':
    # keys=DB.keys('paper*')
    # for k in keys:
    #     print k[6:]
    #     data=DB.get(k)
    #     getCit(data,k[6:])
