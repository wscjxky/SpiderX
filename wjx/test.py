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


with open('headers', 'r')as f:
    dic = {}
    ls = f.readlines()
    for l in ls:
        l = l.strip('\n')
        arr = (l.split(':'))
        dic[arr[0]] = arr[1][1:]
    headers =dic
with open('param', 'r')as f:
    dic = {}
    ls = f.readlines()
    for l in ls:
        l = l.strip('\n')
        arr = (l.split(': '))
        dic[arr[0]] = arr[1]
    params = parse.urlencode(dic)
    params=params.replace('+',"%20")
t = (str(int(time() * 1000)))
proxies = {
'http': 'http://113.251.223.19:8123','https':'111.226.228.202:8118'
}
starttime = (strftime("%Y/%m/%d %H:%M:%S", localtime()))
times={
    't':t,
    'starttime':starttime
}
times=parse.urlencode(times)
print(t)
data = {'submitdata': '1$1'}

url = 'https://www.wjx.cn/joinnew/processjq.ashx?%s&%s'%(params,times)
print(url)
res = requests.post((url), parse.urlencode(data), headers=headers)
print(res.text)
