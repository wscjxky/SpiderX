# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# """
# 自动填问卷星（http://www.sojump.com）
# 单项选择
# """
#
# # 抓包软件： $ sudo apt-get install tshark
# # 打开页面如： http://www.sojump.com/jq/4725800.aspx
# # 随便填写，但不要提交
# # $ sudo tshark -V -i eth0 -f tcp -Y http.request.method=="POST"
# # －V 是解析包的所有信息并打印出来， －i 选择设备接口， -f 抓包过滤， -Y 显示过滤
# # 打印出HTTP POST请求包的所有内容
# # 需要的内容：[Full request URI: http://www.sojump.com/handler/processjq.ashx?
# # submittype=1&curID=186257&t=1428725165556&starttime=2015%2F4%2F11%2012%3A01%3A20&rn=1932211292]
# # [HTTP request 1/1] xxx
# # submitdata=1%241%7D2%242%7D3%243%7D4%241%7D5%242%7D6%243
# # 将上述内容解码（http://tool.chinaz.com/Tools/URLEncode.aspx）
# # 得到 submitdata=1$1}2$2}3$3}4$1}5$2}6$3
#
# # 举例： http://www.sojump.com/jq/4725800.aspx
#
#
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

while True:
    # with open('a', 'r')as f:
    #     dic = {}
    #     ls = f.readlines()
    #     for l in ls:
    #         l = l.strip('\n')
    #         arr = (l.split(':'))
    #         dic[arr[0]] = arr[1][1:]
    t = quote(str(int(time() * 1000)))
    proxies = {
    'http': 'http://113.251.223.19:8123','https':'111.226.228.202:8118'
    }
    starttime = quote(strftime("%Y/%m/%d %H:%M:%S", localtime()))
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 'Connection': 'keep-alive',
               'Content-Length': '296', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'www.wjx.cn',
               'Origin': 'https//www.wjx.cn', 'Referer': 'https://www.wjx.cn/jq/38991650.aspx',
               'User-Agent': 'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 '}
    data = {
        'submitdata': '1$2}2$2}3$3}4$1}5$%s}6$%s}7$%s}8$%s}9$%s}10$6}11$%s}12$6}13$%s}14$7}15$7}16$1}17$7}18$6}19$7}20$6}21$7}22$7}23$6}24$7}25$7}26$%s}27$%s}28$%s}29$%s}30$%s}31$%s}32$%s}33$7' % (
             random.randint(1, 2),  random.randint(1, 2), random.randint(6, 7), random.randint(6, 7), random.randint(6, 7), random.randint(6, 7),
        random.randint(6, 7), random.randint(6, 7), random.randint(6, 7), random.randint(6, 7),
        random.randint(6, 7), random.randint(6, 7), random.randint(6, 7), random.randint(6, 7)
        )}
    url = 'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&source=directphone&curID='\
    '38991650&t=1557361102700&starttime=2019%2F5%2F9%208%3A10%3A46&ktimes=166&rn=3671054072.39690614&hlv=1'\
    '&jqnonce=630c4d5c-9b83-4617-b9b4-18805f270443&jqsign=056e2b3e%2B%3Fd%3E5%2B2071%2Bd%3Fd2%2B7%3E%3E63%60416225'
    # %('1557361102700','2019%2F5%2F9%208%3A10%3A46','3671054072.39690614'
#  ,'630c4d5c-9b83-4617-b9b4-18805f270443','056e2b3e+?d>5+2071+d?d2+7>>63`416225')
    print(url)
    res = requests.post((url), parse.urlencode(data), headers=headers)
    print(res.text)
    sleep(70)
