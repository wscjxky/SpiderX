import requests
from lxml import etree

from robclass.config import headers_image


def get_proxy():
    return (requests.get("http://127.0.0.1:5010/get/").content).decode('utf8')


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# ip地址查询的全代码
import requests

proxy = get_proxy()
print(proxy)
url = 'http://httpbin.org/get'
res = requests.get(url,
                   headers=headers_image,
                   proxies={"http": "http://{}".format(proxy)}
                   )

content = res.text
print(content)
