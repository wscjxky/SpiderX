# -*- coding: utf-8 -*- #

'''
爬虫程序中的坑使用redis数据库，详细操作都在nosql.py中，这文件编写年代久远。。
katoon文件夹用于爬取漫画
edm文件夹用户爬取网易云用户以及喜爱的歌曲
song文件夹用于爬取歌词
'''


#完美编码问题 使用urllib2.urlopen().info()nfo方法查看是否压缩了
#StringIO用来作为字符串的缓存当成文件操作
#gzip解压必须用文件接口
# data = StringIO.StringIO(text)
# gzipper = gzip.GzipFile(fileobj=data) #因为有些网站会压缩网页，这里就是压缩了的
# html = gzipper.read()
# from_encoding 参数来指定编码方式
# 对于大部分非utf8编码中文网站可以用gb18030通吃
# soup = BeautifulSoup(html, fromEncoding='gb18030')

# 很有意思的编码正则
# re_chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
# re_korean_words=re.compile(u"[\uac00-\ud7ff]+")
# re_janpan1_words = re.compile(u"[\u30a0-\u30ff]+")
# re_janpan2_words = re.compile(u"[\u3040-\u309f]+")
# m = re_korean_words.search(s, 0)

# 处理cookie(万能方法模拟浏览器活动)
# from selenium import webdriver
# import time
# username=15281106
# password=15281106 #可能需要输入字符串
# driver =webdriver.Chrome(executable_path="E:\chromed\Chromedriver.exe")
# browser.execute_script("name_text = document.getElementById('name_text');" + "name_text.focus();")
# Ph会有开不了的JSantomJS的，因此需要firefox代替，且目前selenium推荐使用handless浏览器
# driver =webdriver.PhantomJS(executable_path="E:\PyGame\phantomjs\phantomjs.exe")
# driver.get('http://www.baidu.com')
# # driver.find_element_by_id("username").clear()
# # driver.find_element_by_id("password").clear()
# # driver.find_element_by_id("username").send_keys(username)
# # driver.find_element_by_id("password").send_keys(password)
# # driver.find_element_by_css_selector("div>input[value='登录']").click()#css选择器可以在chrome里调试格式 $("主标签>次标签[属性='']")
# savecookies=driver.get_cookies()
# print(savecookies)
# driver.quit()

# #最牛b的firefox handless
# from selenium.webdriver import Firefox
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as expected
# from selenium.webdriver.support.wait import WebDriverWait
# from constant import *
#
# def requestByFixfox(url):
#     time.sleep(TIME_SLEEP)
#     options = Options()
#     options.add_argument('-headless')
#     driver = Firefox(executable_path='geckodriver', firefox_options=options)
#     wait = WebDriverWait(driver, timeout=5)
#     driver.get(url)
#     wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'songNameA')))
#     data= driver.page_source
#     driver.quit()
#     return data
#
# driver1 =webdriver.Chrome(executable_path="E:\chromedriver\chromedriver.exe")
# driver1.get("http://202.112.147.70/moodle/")
# driver1.delete_all_cookies()
# for cookie in savecookies:
# driver1.add_cookie(cookie)
# driver1.quit()
# time.sleep(1)
# driver2 =webdriver.Chrome(executable_path="E:\chromedriver\chromedriver.exe")
# driver2.get("http://202.112.147.70/moodle/")
# print(i.get_attribute(('onclick')))

# 一般方法（post方法）
# import urllib2
# import urllib
# import cookielib
## hosturl = 'http://202.112.147.70/moodle/'
# posturl = 'http://202.112.147.70/moodle/login/index.php'#从开发者工具获得，post网页不用于host,常见的有php,js
# # very important cookie ,if no use,the program no sence
# cj = cookielib.LWPCookieJar()
# cookie_support = urllib2.HTTPCookieProcessor(cj)
# opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
# urllib2.install_opener(opener)
#
## h = urllib2.urlopen(hosturl)
#
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# ,'Referer','http://www.rosiok.com'}
# postData = {'username':15281106,
#             'password':15281106
# }
# postData = urllib.urlencode(postData)#把字典转换成post需要的字符串
# request = urllib2.Request(posturl, postData, headers)  #(url,data=NONE,headers)
# response = urllib2.urlopen(request)
# text = response.read()
# print(text)

# 代理IP(需要配合tor)
# import socks
# import socket
# import urllib2
# url='http://ip.chinaz.com/getip.aspx'
# socks.set_default_proxy(socks.SOCKS5,"localhost",9150)
# socket.socket=socks.socksocket
# print(urllib2.urlopen('http://www.baidu.com').read())
# def getIp():
#     url = 'http://www.xicidaili.com/wt/'
#     req = urllib2.Request(url,headers=Headers)
#     res = urllib2.urlopen(req).read()
#
#     soup = BeautifulSoup(res, 'html.parser')
#     ips = soup.findAll('tr')
#     with open("proxy.txt","w") as f:
#         for x in range(1,len(ips)):
#             ip = ips[x]
#             tds = ip.findAll("td")
#             ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
#             f.write(ip_temp)

# import requests
# print requests.get(test_url, proxies={'http': 'http://27.213.71.159:8118'}).text
# def getValueip():
#                 with open("proxy.txt") as f:
#                     lines = f.readlines()
#                     proxys = []
#                     for i in range(0, len(lines)):
#                         ip = lines[i].strip("\n").split("\t")
#                         proxy_host_safe = "https://" + ip[0] + ":" + ip[1]
#                         proxy_host_unsafe = "http://" + ip[0] + ":" + ip[1]
#                         proxy_temp = {"http": proxy_host_unsafe}
#                         proxys.append(proxy_temp)
#                     url = "http://ip.chinaz.com/getip.aspx"
#                     num = random.randint(0, 80)
#                     print proxys[num]
#                     # return proxys[num]
#                     for proxy in proxys:
#                         print proxy
#                         try:
#                             proxy_support = urllib2.ProxyHandler(proxy)
#                             opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#                             urllib2.install_opener(opener)  # 安装opener，此后调用urlopen()时都会使用安装过的opener对象
#                             response = urllib2.urlopen(url)
#                             print response.read()
#                             return proxy
#                              if(response.read()!="{ip:'223.72.89.23',address:'北京市 移动'}"):
#                     return  proxy
                # print response.read()
#                         except Exception, e:
#                             print 'proxy'
#                             print e
#                             continue
#错误处理
#    try:
#         data = urllib2.urlopen(url)
#     except urllib2.HTTPError,e:
#         if hasattr(e,'code'):
#             if(e.code==403):
#                 # 更换IP
#                 pass
#             elif(e.code==404):
#                 break
#     except Exception ,e:
#         pass
#
 # 比较简单的代理。
# # import urllib2
# # proxy = urllib2.ProxyHandler({'http':'http://218.76.106.78:3128'})#免费/可以做个循环,if判断是否可以用
# # opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
# # urllib2.install_opener(opener)
# # text = urllib2.urlopen('http://www.baidu.com/').read()
# # print(text)
#
# #给模拟器firefoxhandless加代理
# # def imitateClick2(Url,Ipurl,Proxys=None):
# #     Proxytype = "MANUAL"
# #     user_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',)
# #     for Pro in Proxys:
# #         phan_args = ['--proxy=%s'%Pro, '--proxy-type=%s'%Proxytype] #manual手动指定的
# #         dcap = dict(DesiredCapabilities.PHANTOMJS)
# #         dcap["phantomjs.page.settings.userAgent"] = user_agent
# #         driver = webdriver.PhantomJS(executable_path="E:\PyGame\phantomjs\phantomjs.exe",service_args=phan_args, desired_capabilities=dcap)
# #         print('set ok')
# #         driver.get(Url)
# #         print(driver.page_source)
# #         driver.get(Ipurl)
# #         print(driver.page_source)
#
#
# #尝试着多线程抓取合理运用资源
# #三个方法创建线程的3个方法
# # 1，threading.Thread(fun,args)
# # 2, 创建一个由 __call__ 方法的类。
# # 3，继承threading.Thread类，并重写run方法。
# #下面使用类方法
# # import urllib2, time
# # import threading
# # class MyThread(threading.Thread):
# #   def __init__(self, func, args):
# #     threading.Thread.__init__(self)
# #     self.args = args
# #     self.func = func
# #
# #   def run(self):
# #     apply(self.func, self.args) #apply就把run里的参数args传入fun中---url
# # def open_url(url):
# #   request = urllib2.Request(url)
# #   html = urllib2.urlopen(request).read()
# #   print len(html)
# #   return html
# # if __name__ == '__main__':
#
# #   # 构造urllist
# #   urlList = []
# #   for p in range(1, 5):
# #     urlList.append('http://s.wanfangdata.com.cn/Paper.aspx?q=%E5%8C%BB%E5%AD%A6&p=' + str(p))
# #   # 多线程 大好处，单线程编程，只要其中一个数据处理失败，总的直接打断
# #   t_start = time.time()
# #   threadList=[]
# #   for url in urlList:
# #     threadList.append(MyThread(open_url, (url,)))
# #     #优雅的写法threadList = [MyThread(open_url, (url,)) for url in urlList]
# #     #很有意思，python元组只有一个时候就是(12,)不然(12)会被认为是12
# #   for t in threadList:
# #     # 主线程在所有非守护线程都死亡后才会死掉 那么子线程变成孤儿跟父线程干瞪眼形成死循环
# #     # 主要是防止爬取遗漏，对程序运行不影响
# #     t.setDaemon(True)
# #     # 设置守护线程，父线程不必等待子线程执行完后再退出 .类似于垃圾回收
# #     # 别名叫做服务线程，在没有需要它服务的其他线程之后会自杀
# #     t.start()
# #   for i in threadList:
# #   # 如果不要的话 抛出错误 most likely raised during interpreter shutdown 主线程不等子线程就结束了
# #     i.join()        #线程的join方法被call
# #因为有setdaemon主线程不等待子线程，而是在退出时自动结束所有的子线程，就需要设置子线程为后台线程(daemon)
# #python 默认参数创建线程后，不管主线程是否执行完毕，都会等待子线程执行完毕才一起退出，有无join结果一样
# #join方法的作用是阻塞，等待子线程结束
# #     #依次检验线程池中的线程是否结束，没有结束就阻塞此语句直到线程结束，如果结束则跳转执行下一个线程的join函数。直到所有线程结束，结束！进程
# #   t_end = time.time()
# #   print 'the thread way take %s s' % (t_end-t_start)
# #封装
# # def startthread(threadlist,fucname,urllist,):
# #
# #     for i in urllist:
# #         threadlist.append(MyThread(fucname,(i,)))
# #     for t in threadlist:
# #         t.setDaemon(True)  #如果你在for循环里用，不行， 因为上一个多线程还没结束又开始下一个
# #         t.start()
# #     for j in threadlist:
# #         j.join()
#
# #测试系统中可以开辟的最大线程数
# #测试最大线程
# import threading
# import time, random,  sys
#
# class Counter:
#     def __init__(self):
#         self.lock = threading.Lock()
#         self.value = 0
#
#     def increment(self):
#         self.lock.acquire()
#         self.value = value = self.value + 1
#         self.lock.release()
#         return value
#
# counter = Counter()
# cond = threading.Condition()
#
# class Worker(threading.Thread):
#
#     def run(self):
#         print self.getName(),  "-- created."
#         cond.acquire()
#         #for i in range(10):
#             # pretend we're doing something that takes 10?00 ms
#             #value = counter.increment()
#             # time.sleep(random.randint(10, 100) / 1000.0)
#         cond.wait()
#         #print self.getName(), "-- task", "finished"
#         cond.release()
#
#
#
# if __name__ == '__main__':
#
#         try:
#             for i in range(3500):
#                 Worker().start() # start a worker
#         except BaseException,  e:
#             print "异常: ", type(e),  e
#             time.sleep(5)
#             print "maxium i=",  i
#         finally:
#             cond.acquire()
#             cond.notifyAll()
#             cond.release()
#             time.sleep(3)
#             print threading.currentThread().getName(),  " quit"
