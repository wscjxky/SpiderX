import random
from urllib import request, parse
from time import time, strftime, localtime, sleep
from urllib.parse import quote
#
# # 返回uri参数字典
# def gen_uri_param():
#     curID = '38991650'  # 问卷号
#     submittype = '1'
#     t = str(int(time() * 1000))
#     starttime = strftime("%Y/%m/%d %H:%M:%S", localtime())
#     rn = '3671054053.89243871'  # 网页源文件的rndnum
#     return locals()
#
#
# # 返回submitdata字符串
# #  ([(1,2),(2,4),(3,1)]) => '1$2}2$4}3$1'
# def gen_post_string(answer):
#     def concat_pair(pair):
#         return '$'.join([str(pair[0]), str(pair[1])])
#
#     tmp_list = []
#     for x in answer:
#         tmp_list.append(concat_pair(x))
#     return '}'.join(tmp_list)
#
#
# jq_base = "http://www.sojump.com/jq/{}.aspx"
# uri_base = "http://www.sojump.com/handler/processjq.ashx?{}"
#
# # answer是这种形式[(1,2),(2,1),(3,5)……]的答案列表，这里答案是随机生成的。
# answer = zip(range(1, 11), [random.randint(1, 4) for x in range(11)])
# # answer_list = [1,2,3,4,1,2,3,4,1,2]
# # answer = zip(rangeanswer(1,11), answer_list)
# answer="1$1}2$2}3$3}4$2}5$2}6$7}7$7}8$6}9$7}10$6}11$5}12$6}13$7}14$7}15$7}16$1}17$7}18$6}19$7}20$6}21$7}22$7}23$6}24$7}25$7}26$6}27$7}28$7}29$6}30$6}31$6}32$7}33$7"
# post_data = parse.urlencode({'submitdata': (answer)})
# get_data = parse.urlencode(gen_uri_param())
#
# request_url = uri_base.format(get_data)
# req = request.Request(request_url, post_data.encode())
# result = request.urlopen(req)
# print(result.read().decode())
#
# # 打印结果如： 10〒/wjx/join/complete.aspx?q=4725800&JoinID=353793885&jidx=60
# # 拼好链接访问即可看到投票结果 http://www.sojump.com/wjx/join/complete.aspx?q=38991650&JoinID=102681627295&jidx=202....
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
res = requests.post((url), parse.urlencode(data), headers=headers)
print(res.text)
