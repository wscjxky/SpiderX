# -*- coding: utf-8 -*- #用于显示中文
#Gzip视情况而用
import urllib
from bs4 import BeautifulSoup
import gzip
import StringIO
import linecache
from Thread import *
import socket
import os
from SQL import *
import re

import xlrd
import xlutils.copy
import xlwt
import xlsxwriter
class WriteData:
    def __init__(self):
        self.Data=Data
def writeData(Filename,Data,Way='w'):
    if Way=='w':
        File = open(Filename,'w')
        File.write(Data)
        File.close()
    if Way=='a':
        File = open(Filename,'a')
        File.write(Data+'\n')
        File.close()
def readData(Filename,start_Line=None,end_Line=None,Step=None,Way='all'):
    if Way=='all':
        File = open(Filename,'r')
        Data=File.read()
        File.close()
        return Data
    if Way=='line':
        Datalist=[]
        for line in range(start_Line,end_Line,Step):
            Data=linecache.getline(Filename,line)
            Datalist.append(Data)
        return Datalist
def getUrldata(Url,Way='GET',Departure=None,Destination=None):
    time.sleep(1)
    SUCCESS=False
    Attempts=0
    Headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    if (Way=='GET'):
        Req = urllib2.Request(Url,headers=Headers)
        try:
            Text = urllib2.urlopen(Req).read()
        except UnicodeDecodeError as e:
            try:
                Text = urllib2.urlopen(Req).read()
                data = StringIO.StringIO(Text)
                gzipper = gzip.GzipFile(fileobj=data)
                html = gzipper.read()
                return html
            except:
                print('UnicodeDecodeError url:',Url)
        except urllib2.URLError as e:
            print("urlError url:",Url)
            Url=raw_input("re_enter url:")
            getUrldata(Url)
        except socket.timeout as e:
            while(Attempts<3 and not SUCCESS):
                try:
                    getUrldata(Url)
                    SUCCESS=True
                except:
                    Attempts+=1
                    if Attempts==3:
                        exit(0)
                        print("socket timout:",Url)
        else:
            return Text
    elif(Way=='POST'):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        Headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',}
        postData={'DCity':'%s'%tranName(Departure),'RCity':'%s'%tranName(Destination),'DDate':'2016-10'}
        urllib2.install_opener(opener)
        try:
            postData = urllib.urlencode(postData)#把字典转换成post需要的字符串
            request = urllib2.Request(url, postData, Headers)  #(url,data=NONE,headers)
            response = urllib2.urlopen(request).read()
            if not response:
                print('input error,try again')
                exit()
            return response
        except urllib2.URLError,e:
            raise e
    #   gzip类型
    # except:

def getTitlelist(Data,way=None):
    Soup=BeautifulSoup(Data,'html.parser')
    Stringlist=[]
    if('link' in way):
        Tag=Soup.find_all('a',target=True)
        for Strings in Tag:         #Strings.get('title')
            for Str in Strings:
                Stringlist.append(Str)
                print(Str)
        if not(list_is_null(Stringlist)):
            return Stringlist
    if('img' in way):
        Tag=Soup.find_all('img')
        for Strings in Tag:
            print(Strings.get('alt'))
            Stringlist.append(Strings.get('alt'))
        if not(list_is_null(Stringlist)):
            return Stringlist
def downloadImg(Dirname,Imgnum,Urllist):
    if os.path.exists(Dirname)==False:
        os.mkdir(Dirname)
    for Url in Urllist:
        SUCCESS=False
        Attempts=0
        AttemptsMAX=8
        Imgtype=Url[-3:]
        if(Imgtype=='jpg' or Imgtype=='png'):
            while(SUCCESS==False and Attempts<AttemptsMAX):
                try:
                    Request = urllib2.Request(Url)
                    Request.add_header('Referer','http://www.baidu.com')
                    Request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
                    Response = urllib2.urlopen(Request)
                    Data = Response.read()
                    SUCCESS=True
                    File = open("%s/%s.%s" % (Dirname,str(Imgnum),Imgtype),"wb")
                    File.write(Data)
                    File.close()
                    Imgnum+=1
                except:
                    Attempts+=1
def tranName(Name):
    Dic={'北京':'(PEK)','上海':'(SHA)','福州':'(FOC)','杭州':'(HGH)','宁波':'(NGB)'
         ,'天津':'(TSN)','厦门':'(XMN)','广州':'(CAN)'}
    if(Dic.has_key(Name)):
        return Name+Dic[Name]
    else:
        print ("None corresponding name")
        return False
def tranData(Data,Way):
    Data1=Data.strip('[]')
    Datalist=[]
    Str=''
    try:
        for i in Data1:
            if (i==','):
                Datalist.append(Str.strip('""'))
                Str=''
                continue
            Str=Str+i
    except EOFError as e:
        raise e
    except IndexError as e:
        raise e
    else:
        if(Way=='price'):
            for i in Datalist:
               Datalist.remove(i)
        if(Way=='date'):
            for j in range(1,(len(Datalist)/2)):
                Datalist.pop(j)
    return Datalist
def createxcel(Filename,Sheetname):
    workbook = xlwt.Workbook()
    workbook.add_sheet(Sheetname)
    workbook.save(Filename)
def writeExcel(Filename,Datalist,Datalist1,Num_row=0,Num_col=0):
    if not os.path.exists(Filename):
        workbook = xlwt.Workbook()
        workbook.add_sheet(Filename)
        workbook.save(Filename)
    workbook = xlsxwriter.Workbook('chart.xlsx')
    try:
        worksheet = workbook.add_worksheet()
    except IOError as e:
        raise e
    except NameError as e:
        raise e
    else:
        try:
            worksheet.write_column('A1',Datalist)
            worksheet.write_column('B1',map(int,Datalist1))
            chart = workbook.add_chart({'type': 'line'})
            chart.add_series({'values': '=Sheet1!$B$1:$B$30'})
            worksheet.insert_chart('F1', chart)
        except AttributeError as e:
            raise e
        except UnicodeError as e:
            raise e
        except IOError as e:
            raise e
    finally:
        workbook.close()
        print("save")
if __name__ == '__main__':
    # http://brand.efu.com.cn/list-1-0-0-0-0-0-1.html
    # http://www.gldjc.com/
    # Data=getUrldata('http://www.syuntravel.cn/PassengerTicket/SearchHistoryTicket')
    url='http://www.syuntravel.cn/PassengerTicket/SearchHistoryTicket'
    # Data=getUrldata(url,Way='POST',Departure='北京',Destination='上海')
    Data='["2016/10/1 0:00:00","679","2016/10/2 0:00:00","528","2016/10/3 0:00:00","430","2016/10/4 0:00:00","314","2016/10/5 0:00:00","407","2016/10/6 0:00:00","409","2016/10/7 0:00:00","440","2016/10/8 0:00:00","469","2016/10/9 0:00:00","312","2016/10/10 0:00:00","309","2016/10/11 0:00:00","510","2016/10/12 0:00:00","510","2016/10/13 0:00:00","510","2016/10/14 0:00:00","550","2016/10/15 0:00:00","480","2016/10/16 0:00:00","469","2016/10/17 0:00:00","520","2016/10/18 0:00:00","500","2016/10/19 0:00:00","547","2016/10/20 0:00:00","593","2016/10/21 0:00:00","593","2016/10/22 0:00:00","500","2016/10/23 0:00:00","535","2016/10/24 0:00:00","499","2016/10/25 0:00:00","542","2016/10/26 0:00:00","596","2016/10/27 0:00:00","593","2016/10/28 0:00:00","570","2016/10/29 0:00:00","480","2016/10/30 0:00:00","479","2016/10/31 0:00:00","409"]'
    writeExcel('b.xls',tranData(Data,Way='date'),tranData(Data,Way='price'))

