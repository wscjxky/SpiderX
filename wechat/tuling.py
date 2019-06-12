#coding=utf8
import re
import socket
import sys, os
import urllib.parse,urllib.request


import requests, json

try:
    with open('tuling.json') as f: key = json.loads(f.read())['key']
except:
    key = '' # if key is '', get_response will return None
    # raise Exception('There is something wrong with the format of you plugin/config/tuling.json')

def get_response(msg, storageClass = None, userName = None, userid = 'ItChat'):
    url = 'http://www.tuling123.com/openapi/api'
    payloads = {
        'key': key,
        'info': msg,
        'userid': userid,
    }
    try:
        r = requests.post(url, data = json.dumps(payloads)).json()
        print(r)
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000: # 文本类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 200000: # 链接类
        return '\n'.join([r['text'].replace('<br>','\n'), r['url']])
    elif r['code'] == 302000: # 新闻类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['article'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 308000: # 菜谱类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['name'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 313000: # 儿歌类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 314000: # 诗词类
        return '\n'.join([r['text'].replace('<br>','\n')])
def qingyun_res(text):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s'%text

    r = requests.get(url).json()
    return r['content']
def dou_res(text):
    url_api = "http://api.douqq.com?key=MlVZZjR3N0ZqVj1ISXBZTG1RVDBMMEI9VEJjQUFBPT0&msg=" + text
    a=requests.get(url_api)
    print(a.content)
    out_str = str(a.content, encoding="utf-8")
    print(out_str)
def format_func(str_xiaoi):
    str_xiaoi=re.sub("\\\\","",str_xiaoi)
    str_xiaoi=re.sub("[\s\S]*__webrobot_processMsg","msg",str_xiaoi)
    str_xiaoi=re.sub('[\s\S]*\"body\":\{',"msg({",str_xiaoi)
    str_xiaoi=re.sub('[\s\S]*content\":\"',"",str_xiaoi)
    str_xiaoi=str_xiaoi[:-22]
    if re.search(r"\[.+\]",str_xiaoi):
        # 检测到网址
        str_xiaoi=re.sub(r"\[.+http","http",str_xiaoi)
        str_xiaoi=re.sub(r'.]',"",str_xiaoi)
        str_xiaoi=re.sub(r'\[/lin',"",str_xiaoi)
    if re.search("rn",str_xiaoi):
        # 检测到换行符
        str_xiaoi=re.sub("rn","",str_xiaoi)
    if re.search(r"u[0-9abcdef]{4}",str_xiaoi):
        # 检测到HTML编码
        str_xiaoi=re.sub(r"u[0-9abcdef]{4}","",str_xiaoi)
    return str_xiaoi

def xiaoi(text):
    word = urllib.parse.quote(text)
    # 更新网址：
    url_api = "http://i.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22f5b61eba68144a429b543a0d9a98eb90%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%22873a71883fd74449b3c99874cf7ad886%22%2C%22body%22%3A%7B%22content%22%3A%22%E4%BD%A0%E5%A5%BD%22%7D%2C%22type%22%3A%22txt%22%7D&ts=1534051772519"
    # %E4%BD%A0%E5%A5%BD
    url_new = re.sub("%E4%BD%A0%E5%A5%BD", word, url_api)
    timeout = 7
    socket.setdefaulttimeout(timeout)
    req = urllib.request.Request(url_new)
    a = urllib.request.urlopen(req).read()
    main_out_str = str(a, encoding="utf-8")
    main_out_str = format_func(main_out_str)
    return main_out_str
if __name__ == '__main__':
    get_response("呵呵",'ItChat')
    xiaoi("爱你")
    dou_res("123")
