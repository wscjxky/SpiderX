import os

import requests
from bs4 import BeautifulSoup


def get_shop():
    # key='%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%20%E8%87%AA%E9%A1%B6%E5%90%91%E4%B8%8B%E6%96%B9%E6%B3%95%205'
    url = "http://search.kongfz.com/product_result/?select=0&key=%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%20%E8%87%AA%E9%A1%B6%E5%90%91%E4%B8%8B%E6%96%B9%E6%B3%95%205&order=7"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Referer': url,
        'Host': 'search.kongfz.com',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        "X-Requested-With": "XMLHttpRequest",
        # "Connection": "close",
    }

    data = requests.get(url, headers=headers).text
    soup = BeautifulSoup(data, 'html.parser')
    tag_1 = soup.find_all('div', class_="user-info ")
    for tag_2 in tag_1:  # Strings.get('title')
        with open("result/" + url[-15:] + ".txt", 'a')as f:
            href = tag_2.find('a', class_="user-info-link").get('href')
            print(href)
            f.write(href + "\n")

def equal_shop():
    shops = {}
    for root, dirs, files in os.walk("result"):
        for f in files:
            with open("result/" + f, 'r') as f:
                for l in f.readlines():
                    l=l.strip()
                    try:
                        shops[l]
                    except:
                        shops[l] = 0
                        continue
                    if shops[l]==0:
                        shops[l] += 1
    for k,v in shops.items():
        if v>0:
            print(k)


equal_shop()
