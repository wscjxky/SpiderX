#encoding=utf8
import random
import urllib2
from bs4 import BeautifulSoup
import socket

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

socket.setdefaulttimeout(10)
import urllib,requests
import redis
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    ,'Referer': 'http://www.baidu.com/'

}
def getIplist():
    url='http://127.0.0.1:8000/?country=%E5%9B%BD%E5%86%85'
    test_url = "http://www.juzimi.com/"
    json = requests.get(url).json()
    proxys = []
    for i in range(0, len(json)):
        ip=str(json[i][0])
        port=str(json[i][1])
        proxy_host_safe = "https://" + ip + ":" +port
        proxy_host_unsafe = "http://" +ip + ":" + port
        proxy_temp = {"http": proxy_host_unsafe}
        proxy_support = urllib2.ProxyHandler(proxy_temp)
        opener = urllib2.build_opener(proxy_support)
        opener.addheaders = [('User-agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        urllib2.install_opener(opener)
        try:
            s = urllib2.urlopen(test_url).read()
            # if not '未知' in str(s) :
            proxys.append(proxy_temp)
            with open('ip.txt','a+') as f:
                f.write(str(proxy_temp)+"\n")
            print proxy_temp
        except Exception,e:
            print e
    return proxys


def getFreeIp():
    url = 'http://www.xicidaili.com/wt/'
    req = urllib2.Request(url,headers=Headers)
    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup(res, 'html.parser')
    ips = soup.findAll('tr')
    with open("proxy.txt","w") as f:
        for x in range(1,len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
            f.write(ip_temp)


def testIp():
    with open("proxy.txt") as f:
        lines = f.readlines()
        proxys = []
        for i in range(0,len(lines)):
            ip = lines[i].strip("\n").split("\t")
            proxy_host = ip[0]+":"+ip[1]
            proxys.append(proxy_host)
        url = "http://ip.chinaz.com/getip.aspx"
        for proxy in proxys:
            print proxy
            req=urllib2.Request(url,headers=Headers)
            #注意字符串错误
            req.set_proxy(str(proxy),'http')
            res = urllib2.urlopen(req).read()
            print res
            break
def getValueip():
    ip_list=[]
    with open('ip.txt','r')as  f :
        lines=f.readlines()
        for l in lines:
            ip_list.append(eval(l))
    return ip_list

    # with open("proxy.txt") as f:
    #     lines = f.readlines()
    #     proxys = []
    #     for i in range(0, len(lines)):
    #         ip = lines[i].strip("\n").split("\t")
    #         proxy_host_safe = "https://" + ip[0] + ":" + ip[1]
    #         proxy_host_unsafe = "http://" + ip[0] + ":" + ip[1]
    #         proxy_temp = {"http": proxy_host_unsafe}
    #         proxys.append(proxy_temp)
    #     url = "http://ip.chinaz.com/getip.aspx"
    #     aim_url='http://www.juzimi.com/dynasty/%E9%AD%8F%E6%99%8B'
    #     for proxy in proxys:
    #         print proxy
    #         try:
    #             proxy_support = urllib2.ProxyHandler(proxy)
    #             opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    #             urllib2.install_opener(opener)  # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
    #             response = urllib2.urlopen(url)
    #             if(response.read()!="{ip:'223.72.89.23',address:'北京市 移动'}"):
    #                 print response.read()
    #                 proxy_support = urllib2.ProxyHandler(proxy)
    #                 opener = urllib2.build_opener(proxy_support)
    #                 urllib2.install_opener(opener)
    #                 source=urllib2.urlopen(aim_url).read()
    #                 if '无效用户' not in source and '有道' not in source :
    #                     return proxy
    #             print response.read()
    #             # num=random.randint(0,80)
    #             # return proxy[num]
    #         except urllib2.HTTPError, e:
    #             if hasattr(e, 'code'):
    #                 if (e.code == 403):
    #                     # 更换IP
    #                     pass
    #                 elif (e.code == 404):
    #                     pass
    #                     # break
    #         except Exception, e:
    #             print 'proxy'
    #             print e
    #             continue
# req = urllib2.Request('http://www.juzimi.com/dynasty/先秦', headers=Headers)
# 注意字符串错误

# req.set_proxy(getValueip(), 'http')

# try :
#     res = urllib2.urlopen(req).read()
#     print res
# except Exception, e:
#     print e

if __name__ == '__main__':
    test_url = "http://ip.chinaz.com/getip.aspx"
    url='http://music.163.com/'
    # proxy = getIp()
    proxy={'http': 'http://39.134.93.13:80'}

#
    print proxy
#    ip_list=getValueip()
# url='http://www.juzimi.com/'
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
    urllib2.install_opener(opener)
    req = urllib2.Request(url, headers=Headers)
    s = urllib2.urlopen(req).read()
    print s
# # try:

#
#
#     # import requests
#     #
#     # print requests.get(test_url, proxies={'http': 'http://27.213.71.159:8118'}).text
# l= [u'\u5c71\u4e00\u7a0b\uff0c\u6c34\u4e00\u7a0b\uff0c\u8eab\u5411\u6986\u5173\u90a3\u7554\u884c\uff0c\u591c\u6df1\u5343\u5e10\u706f\u3002 \r\u98ce\u4e00\u66f4\uff0c\u96ea\u4e00\u66f4\uff0c\u8052\u788e\u4e61\u5fc3\u68a6\u4e0d\u6210\uff0c\u6545\u56ed\u65e0\u6b64\u58f0\u3002', u'\u4e00\u5f80\u60c5\u6df1\u6df1\u51e0\u8bb8\uff1f\r\u6df1\u5c71\u5915\u7167\u6df1\u79cb\u96e8\u3002', u'\u6d6e\u751f\u82e5\u68a6\uff0c\u522b\u591a\u4f1a\u5c11\uff0c\u4e0d\u5982\u83ab\u9047\u3002', u'\u4e00\u751f\u4e00\u4ee3\u4e00\u53cc\u4eba\uff0c\u4e89\u6559\u4e24\u5904\u9500\u9b42\u3002', u'\u4e00\u751f\u4e00\u4ee3\u4e00\u53cc\u4eba\uff0c\u4e89\u6559\u4e24\u5904\u9500\u9b42\u3002', u'\u6211\u662f\u4eba\u95f4\u60c6\u6005\u5ba2\uff0c\u65ad\u80a0\u58f0\u91cc\u5fc6\u5e73\u751f', u'\u534a\u4e16\u6d6e\u840d\u968f\u901d\u6c34\uff0c\u4e00\u5bb5\u51b7\u96e8\u846c\u540d\u82b1\u3002', u'\u4eba\u751f\u82e5\u53ea\u5982\u521d\u89c1\uff0c\r\u4f55\u4e8b\u79cb\u98ce\u60b2\u753b\u6247\u3002\r\u7b49\u95f2\u53d8\u5374\u6545\u4eba\u5fc3\uff0c\r\u5374\u9053\u6545\u4eba\u5fc3\u6613\u53d8\u3002', u'\u4e00\u751f\u6070\u5982\u4e09\u6708\u82b1\uff0c\r\u503e\u6211\u4e00\u751f\u4e00\u4e16\u5ff5\uff0c\u6765\u5982\u98de\u82b1\u6563\u4f3c\u70df\r\u9189\u91cc\u4e0d\u77e5\u5e74\u534e\u9650\uff0c\u5f53\u65f6\u82b1\u524d\u98ce\u8fde\u7fe9 \r\u51e0\u8f6e\u6625\u5149\u5982\u7389\u989c \r\u6e05\u98ce\u4e0d\u89e3\u8bed\uff0c\u600e\u77e5\u98ce\u5149\u604b \r\u4e00\u6837\u82b1\u5f00\u4e00\u5343\u5e74\uff0c\u72ec\u770b\u6ca7\u6d77\u5316\u6851\u7530\r\u4e00\u7b11\u671b\u7a7f\u4e00\u5343\u5e74\uff0c\u7b11\u5bf9\u7e41\u534e\u5c18\u4e16\u95f4 \r\u8f7b\u53f9\u67f3\u8001\u4e0d\u5439\u7ef5\uff0c\u77e5\u541b\u5230\u8eab\u8fb9\r-', u'\u4e00\u751f\u4e00\u4e16\u4e00\u53cc\u4eba\uff0c\u534a\u9189\u534a\u9192\u534a\u6d6e\u751f\u3002', u'\u6fb9\u82b1\u7626\u7389\u8f7b\u5986\u675f\uff0c\u7c89\u878d\u8f7b\u6c57\u7ea2\u7ef5\u6251\u3002\u5986\u7f62\u53ea\u6c34\u7720\uff0c\u6c5f\u5357\u56db\u6708\u5929\u3002\r \u7eff\u9634\u5e18\u534a\u63ed\uff0c\u6b64\u666f\u6e05\u5e7d\u7edd\u3002\u884c\u5ea6\u7af9\u6797\u98ce\uff0c\u5355\u886b\u674f\u5b50\u7ea2\u3002', u'\u534a\u4e16\u6d6e\u840d\u968f\u901d\u6c34\uff0c\u4e00\u5bb5\u51b7\u96e8\u846c\u540d\u82b1\u3002\u9b42\u662f\u67f3\u7ef5\u5439\u6b32\u788e\uff0c\u7ed5\u5929\u6daf\u3002', u'\u96fe\u7a97\u5bd2\u5bf9\u9065\u5929\u66ae\uff0c\u66ae\u5929\u9065\u5bf9\u5bd2\u7a97\u96fe\u3002\u82b1\u843d\u6b63\u557c\u9e26\uff0c\u9e26\u557c\u6b63\u843d\u82b1\u3002   \r\u8896\u7f57\u5782\u5f71\u7626\uff0c\u7626\u5f71\u5782\u7f57\u8896\u3002\u98ce\u7fe6\u4e00\u4e1d\u7ea2\uff0c\u7ea2\u4e1d\u4e00\u7fe6\u98ce\u3002', u'\u8f9b\u82e6\u6700\u601c\u5929\u4e0a\u6708, \u4e00\u5915\u5982\u73af,\u5915\u5915\u957f\u6210\u73a6!', u'\u94f6\u5e8a\u6dc5\u6ca5\u9752\u68a7\u8001\uff0c\u5c67\u7c89\u79cb\u86e9\u626b\u3002\u91c7\u9999\u884c\u5904\u8e59\u8fde\u94b1\uff0c\u62fe\u5f97\u7fe0\u7fd8\u4f55\u6068\u4e0d\u80fd\u8a00\u3002\r\u56de\u5eca\u4e00\u5bf8\u76f8\u601d\u5730\uff0c\u843d\u6708\u6210\u5b64\u501a\u3002\u80cc\u706f\u548c\u6708\u5c31\u82b1\u9634\uff0c\u5df2\u662f\u5341\u5e74\u8e2a\u8ff9\u5341\u5e74\u5fc3\u3002', u'\u4e07\u5e10\u7a79\u5e90\u4eba\u9189,\u661f\u5f71\u6447\u6447\u6b32\u5760.\u5f52\u68a6\u9694\u72fc\u6cb3,\u53c8\u88ab\u6cb3\u58f0\u6405\u788e.\u8fd8\u7761,\u8fd8\u7761,\u89e3\u9053\u9192\u6765\u65e0\u5473.', u'\u80cc\u706f\u548c\u6708\u5c31\u82b1\u9634\uff0c\u5df2\u662f\u5341\u5e74\u8e2a\u8ff9\u5341\u5e74\u5fc3', u'\u4eba\u5230\u60c5\u591a\u60c5\u8f6c\u8584\uff0c\u800c\u4eca\u771f\u4e2a\u4e0d\u591a\u60c5 \xa0\xa0', u'\u800c\u4eca\u624d\u9053\u5f53\u65f6\u9519\uff0c\u5fc3\u7eea\u51c4\u8ff7\u3002\u7ea2\u6cea\u5077\u5782\uff0c\u6ee1\u773c\u6625\u98ce\u767e\u4e8b\u975e\u3002\r\u60c5\u77e5\u6b64\u540e\u6765\u65e0\u8ba1\uff0c\u5f3a\u8bf4\u6b22\u671f\u3002\u4e00\u522b\u5982\u65af\uff0c\u843d\u5c3d\u68a8\u82b1\u6708\u53c8\u897f\u3002', u'\u98ce\u4e1d\u8885\uff0c\u6c34\u6d78\u78a7\u5929\u6e05\u6653\u3002\u4e00\u955c\u6e7f\u4e91\u6e05\u672a\u4e86\uff0c\u96e8\u6674\u6625\u8349\u8349\u3002\r\u68a6\u91cc\u8f7b\u87ba\u8c01\u626b\u3002\u5e18\u5916\u843d\u82b1\u7ea2\u5c0f\u3002\u72ec\u7761\u8d77\u6765\u60c5\u6084\u6084\uff0c\u5bc4\u6101\u4f55\u5904\u597d\uff1f\r\u91d1\u4eba\u6367\u9732\u76d8 \u51c0\u4e1a\u5bfa\u89c2\u83b2\uff0c\u6709\u6000\u836a\u53cb\r\u85d5\u98ce\u8f7b\uff0c\u83b2\u9732\u51b7\uff0c\u65ad\u8679\u6536\uff0c\u6b63\u7ea2\u7a97\u3001\u521d\u4e0a\u5e18\u94a9\u3002\u7530\u7530\u7fe0\u76d6\uff0c\u8d81\u659c\u9633\u9c7c\u6d6a\u9999\u6d6e\u3002\u6b64\u65f6\u753b\u9601\u5782\u6768\u5cb8\uff0c\u7761\u8d77\u68b3\u5934\u3002\r\u65e7\u6e38\u8e2a\uff0c\u62db\u63d0\u8def\uff0c\u91cd\u5230\u5904\uff0c\u6ee1\u79bb\u5fe7\u3002\u60f3\u8299\u84c9\u6e56\u4e0a\u60a0\u60a0\u3002\u7ea2\u8863\u72fc\u85c9\uff0c\u5367\u770b\u6843\u53f6\u9001\u5170\u821f\u3002\u5348\u98ce\u5439\u65ad\u6c5f\u5357\u68a6\uff0c\u68a6\u91cc\u83f1\u8bb4\u3002', u'\u78a7\u6d77\u5e74\u5e74\uff0c\u8bd5\u95ee\u53d6\u3001\u51b0\u8f6e\u4e3a\u8c01\u5706\u7f3a\uff1f\u5439\u5230\u4e00\u7247\u79cb\u9999\uff0c\u6e05\u8f89\u4e86\u5982\u96ea\u3002\u6101\u4e2d\u770b\u597d\u5929\u826f\u591c\uff0c\u77e5\u9053\u5c3d\u6210\u60b2\u54bd\u3002\u53ea\u5f71\u800c\u4eca\uff0c\u90a3\u582a\u91cd\u5bf9\uff0c\u65e7\u65f6\u660e\u6708\u3002 \r  \u82b1\u5f84\u91cc\u3001\u620f\u6349\u8ff7\u85cf\uff0c\u66fe\u60f9\u4e0b\u8427\u8427\u4e95\u68a7\u53f6\u3002\u8bb0\u5426\u8f7b\u7ea8\u5c0f\u6247\uff0c\u53c8\u51e0\u756a\u51c9\u70ed\u3002\u53ea\u843d\u5f97\u3001\u586b\u81ba\u767e\u611f\uff0c\u603b\u832b\u832b\u3001\u4e0d\u5173\u79bb\u522b\u3002\u4e00\u4efb\u7d2b\u7389\u65e0\u60c5\uff0c\u591c\u5bd2\u5439\u88c2\u3002', u'\u6797\u4e0b\u8352\u82d4\u9053\u97eb\u5bb6\uff0c\u751f\u601c\u7389\u9aa8\u59d4\u5c18\u6c99\u3002\u6101\u5411\u98ce\u524d\u65e0\u5904\u8bf4\uff0c\u6570\u5f52\u9e26\u3002 \r\u534a\u4e16\u6d6e\u840d\u968f\u6c34\u901d\uff0c\u4e00\u5bb5\u51b7\u96e8\u846c\u540d\u82b1\u3002\u9b42\u662f\u67f3\u7ef5\u5439\u6b32\u788e\uff0c\u7ed5\u5929\u6daf\u3002', u'\u5fb7\u4e5f\u72c2\u751f\u8033\uff0c\r\u5076\u7136\u95f4\u3001\u6dc4\u5c18\u4eac\u56fd\uff0c\u4e4c\u8863\u95e8\u7b2c\uff0c\u6709\u9152\u552f\u6d47\u8d75\u5dde\u571f\uff0c\u8c01\u4f1a\u6210\u751f\u6b64\u610f\uff1f\u4e0d\u4fe1\u9053\u3001\u9042\u6210\u77e5\u5df1\uff0c\u9752\u773c\u9ad8\u6b4c\u4ff1\u672a\u8001\u3002\u5411\u5c0a\u524d\u3001\u62ed\u5c3d\u82f1\u96c4\u6cea\u3002\u541b\u4e0d\u89c1\uff0c\u6708\u5982\u6c34\uff0c\u5171\u541b\u6b64\u591c\u987b\u6c89\u9189\u3002\r\u4e14\u7531\u4ed6\u3001\u5a25\u7709\u8c23\u8bfc\uff0c\u53e4\u4eca\u540c\u5fcc\u3002\u8eab\u4e16\u60a0\u60a0\u4f55\u8db3\u95ee\uff0c\u51b7\u7b11\u7f6e\u4e4b\u800c\u5df2\u3002\u5bfb\u601d\u8d77\u3001\u4ece\u5934\u7ffb\u6094\uff0c\u4e00\u65e5\u5fc3\u671f\u5343\u52ab\u5728\u3002\u540e\u8eab\u7f18\u3001\u6050\u7ed3\u4ed6\u751f\u91cc\u3002\u7136\u8bfa\u91cd\uff0c\u541b\u987b\u8bb0\u3002', u'\u98ce\u4e00\u66f4\uff0c\u96ea\u4e00\u66f4\uff0c\u8052\u788e\u4e61\u5fc3\u68a6\u4e0d\u6210\uff0c\u6545\u56ed\u65e0\u6b64\u58f0', u'\u8fd1\u6765\u65e0\u9650\u4f24\u5fc3\u4e8b\uff0c\u8c01\u4e0e\u8bdd\u957f\u66f4\uff1f\u4ece\u6559\u5206\u4ed8\uff0c\u7eff\u7a97\u7ea2\u6cea\uff0c\u65e9\u96c1\u521d\u83ba\u3002 \r\u5f53\u65f6\u9886\u7565\uff0c\u800c\u4eca\u65ad\u9001\uff0c\u603b\u8d1f\u591a\u60c5\u3002\u5ffd\u7591\u541b\u5230\uff0c\u6f06\u706f\u98ce\u98d0\uff0c\u75f4\u6570\u6625\u661f\u3002', u'\u6cea\u54bd\u66f4\u65e0\u58f0,\u6b62\u5411\u4ece\u524d\u6094\u8584\u60c5.\u51ed\u4ed7\u4e39\u9752\u91cd\u7701\u8bc6,\u76c8\u76c8,\u4e00\u7247\u4f24\u5fc3\u753b\u4e0d\u6210\u3002\r\u522b\u8bed\u5fd2\u5206\u660e,\u5348\u591c\u9e63\u9e63\u68a6\u65e9\u9192.\u537f\u81ea\u65e9\u9192\u4fac\u81ea\u68a6,  \u66f4\u66f4,\u6ce3\u5c3d\u98ce\u524d\u591c\u96e8\u94c3\u3002', u'\u5fc3\u7070\u5c3d\uff0c\u6709\u53d1\u672a\u5168\u50e7\u3002\u98ce\u96e8\u6d88\u78e8\u751f\u6b7b\u522b\uff0c\u4f3c\u66fe\u76f8\u8bc6\u53ea\u5b64\u6aa0\uff0c\u60c5\u5728\u4e0d\u80fd\u9192\u3002\r\u6447\u843d\u540e\uff0c\u6e05\u5439\u90a3\u582a\u542c\u3002\u6dc5\u6ca5\u6697\u98d8\u91d1\u4e95\u53f6\uff0c\u4e4d\u95fb\u98ce\u5b9a\u53c8\u949f\u58f0\uff0c\u8584\u798f\u8350\u503e\u57ce', u'\u51b7\u5904\u504f\u4f73\uff0c\u522b\u6709\u6839\u82bd\uff0c\u4e0d\u662f\u4eba\u95f4\u5bcc\u8d35\u82b1\u3002', u'\u98ce\u7d6e\u98d8\u6b8b\u5df2\u5316\u840d\uff0c\u6ce5\u83b2\u521a\u5029\u85d5\u4e1d\u8426\u3002\u73cd\u91cd\u522b\u62c8\u9999\u4e00\u74e3\uff0c\u8bb0\u524d\u751f\u3002\r\u4eba\u5230\u60c5\u591a\u60c5\u8f6c\u8584\uff0c\u800c\u4eca\u771f\u4e2a\u6094\u591a\u60c5\u3002\u53c8\u5230\u65ad\u80a0\u56de\u9996\u5904\uff0c\u6cea\u5077\u96f6\u3002', u'\u51c4\u51c9\u522b\u540e\u4e24\u5e94\u540c\uff0c\u6700\u662f\u4e0d\u80dc\u6e05\u6028\u6708\u660e\u4e2d\u3002']
# for i in l:
#     print i

# if __name__ == "__main__":
#     # corpus=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开
#     #     "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果
#     #     "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果
#     #     "我 爱 北京 天安门"]#第四类文本的切词结果
#     corpus=['圣诞节 是的 权 我']
#     vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#
#     transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
#     tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
#     word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
#     print word
#
#     weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
#     for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
#         print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"
#         for j in range(len(word)):
#             print word[j],weight[i][j]