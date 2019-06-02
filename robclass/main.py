import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import requests
import threading
import asyncio
from bs4 import BeautifulSoup
import os
import sqlite3
import requests
import time
from multiprocessing import Process,Pool

from win32.win32crypt import CryptUnprotectData
def getcookiefromchrome(host='.oschina.net'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()
        cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        # print(cookies)
        return cookies

def Hack(cookies):
    data = {"Host": "dean.bjtu.edu.cn",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8"
            }
    res = requests.get("https://dean.bjtu.edu.cn/captcha/refresh/", cookies=cookies, headers=data)
    #print(res.text[res.text.find("/captcha") + 15:-3])
    keyvalue = res.text[res.text.find("/captcha") + 15:-3]
    i = 0
    while i <= 100:

        f = {'checkboxs': '83357', 'hashkey': keyvalue, 'answer': str(i)}
        res2 = requests.post("https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit",cookies=cookies, data=f,headers=data)
        if len(res2.text) != 41:
            break;
        i += 1
    re=[keyvalue,i]
    res1 = requests.get("https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/", cookies=cookies)
    soup = BeautifulSoup(res1.text, 'html.parser')
    nowclass = soup.find_all("tr")
    t = 1
    strnow = ''
    while t < len(nowclass):
        if str(nowclass[t]).find("大学生安全教育")!=-1:
            strnow=str(nowclass[t])
            num=strnow[strnow.find("data-pk")+9:strnow.find("data-pk")+15]
            requests.post("https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=delete",cookies=cookies,data={"select_id":num})
            break;
        t+=1
    return re
def GetClass(cookies,num1):
    fs=open('result.txt','w',encoding='utf-8')
    data = {"Host": "dean.bjtu.edu.cn",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8"
            }
    res=requests.get("https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page="+num1,cookies=cookies,headers=data)
    fs.write(res.text)
    soup=BeautifulSoup(res.text,'html.parser')
    #classes=soup.find_all(attrs={"name":"checkboxs","type":"checkbox","class":"checkbox"})
    classess=soup.find_all("tr")
    i=1
    strlist=[]
    while i<len(classess):
        strlist.append(str(classess[i]))
        i+=1
    return strlist
cookies={}#初始化cookies字典变量
header = {"Host": "dean.bjtu.edu.cn",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8"
            }
cookies=getcookiefromchrome('dean.bjtu.edu.cn')
print("请输入抢课页数")
num1=input()
print("请输入抢课序号")
num2=input()
i=0
hacklist = Hack(cookies)
keyvalue=hacklist[0]
answer=hacklist[1]
t0=time.time()
while True:
    classes=GetClass(cookies,num1)
    index=classes[int(num2)-1].find('value')
    if index!=-1:
        f = {'checkboxs': classes[int(num2)-1][index+7:index+12], 'hashkey': keyvalue, 'answer': str(answer)}
        res2=requests.post("https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit",cookies=cookies,data=f,headers=header)
        print("Bingo!")
        print(res2.text)
        break
    else:
        i+=1
        print(i)
        if i%100==0:
            speed=i/(time.time()-t0)
            print('speed: {:.2f}/s'.format(speed))
            hacklist = Hack(cookies)
            keyvalue = hacklist[0]
            answer = hacklist[1]
            print(answer)
os.system("pause")
#print(Hack(cookies))


#
# while
#