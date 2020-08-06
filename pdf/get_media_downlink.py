import urllib.request

import requests

robclass_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
}
from requests_html import HTMLSession
import requests

d = 0


def cbk(a, b, c):
    global  d
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    if d % 100 == 0:
        d = 0
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.2f%%' % per)
    d += 1


def download(download_link, title):
    r = requests.get(download_link, headers=robclass_headers)
    print(r.content)
    with open(title + ".pdf", "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)


def media_download_link(url):
    session = HTMLSession()
    print(url)
    r = session.get(url)
    downLink = r.html.find('.input.popsok')
    if len(downLink)>0:

        downLink = (downLink[0].attrs["href"])
        name = downLink.split('/')[-1]
        print(name)
        urllib.request.urlretrieve(downLink, name, cbk)


fs = open("dllinks.txt", 'r', encoding="utf8")
ls = fs.readlines()
p=0
for l in ls:
    if 'media' in l:
        if p==0:
            p+=1
            continue
        media_download_link(l)
