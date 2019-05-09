import random
from urllib import request, parse
from time import time, strftime, localtime, sleep
from urllib.parse import quote
import requests
import js2py
import re


def encodeURI(string):
    js_res = js2py.eval_js('''function eval_data(string){
       return  encodeURIComponent(string);}''')
    return js_res(string)

def getsign():
    import requests
    curID = 39164517
    submittype = 1
    data = requests.get('https://www.wjx.cn/jq/%s.aspx?from=timeline' % curID)
    hlv = 1
    data = data.text
    jqnonce = re.search('jqnonce="(.*?)"', data).group(1)
    rndnum = re.search('rndnum="(.*?)"', data).group(1)
    starttime = re.search('starttime="(.*?)"', data).group(1)
    t = (str(int(time() * 1000)))
    js_res = js2py.eval_js('''
    function gen(jqnonce, ktimes) {
        var c, d, e, b = ktimes % 10;
        var a = jqnonce;
        for (0 == b && (b = 1), c = [], d = 0; d < a.length; d++) e = a.charCodeAt(d) ^ b,
            c.push(String.fromCharCode(e));
        var jqsign = (c.join(""));
        return jqsign;
    }
    ''')
    ktimes = 58
    jqsign = js_res(jqnonce, ktimes)
    params = {'submittype': submittype,
              'curID': curID,
              't': t,
              'ktimes': ktimes,
              'rn': rndnum,
              'hlv': hlv,
              'jqnonce': jqnonce,
              'starttime': starttime,
              'jqsign': jqsign}
    print(params)
    url = 'https://www.wjx.cn/joinnew/processjq.ashx?from=timeline&%s' \
          % (parse.urlencode(params))
    print(url)
    return url


with open('headers', 'r')as f:
    dic = {}
    ls = f.readlines()
    for l in ls:
        l = l.strip('\n')
        arr = (l.split(':'))
        dic[arr[0]] = arr[1][1:]
    headers = dic
t = (str(int(time() * 1000)))
proxies = {
    'http': 'http://113.251.223.19:8123', 'https': '111.226.228.202:8118'
}
data = {'submitdata': '1$1'}
url = getsign()
sleep(4)
res = requests.post((url), parse.urlencode(data), headers=headers)
print(res.text)
