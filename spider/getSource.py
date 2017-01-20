# -*- coding: utf-8 -*- #用于显示中文
from selenium import webdriver
import urllib2,urllib
import StringIO
import gzip
import socket
from config import *
from  config import CONSTANT as C
from SQL import *
def tranName(Name):
    Dic={'北京':'(PEK)','上海':'(SHA)','福州':'(FOC)','杭州':'(HGH)','宁波':'(NGB)'
         ,'天津':'(TSN)','厦门':'(XMN)','广州':'(CAN)'}
    if(Dic.has_key(Name)):
        return Name+Dic[Name]
    else:
        print ("None corresponding name")
        writeLog(CONSTANT.logfile,"None corresponding name")
        return False
def tranData(Data,Way='date'):
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
        writeLog(C.IOError,"tranData: ")
    except IndexError as e:
        writeLog(C.INDEXError,"tranData: ")
    else:
        if(Way=='price'):
            for i in Datalist:
               Datalist.remove(i)
            for i,value in enumerate(Datalist):
                if value=='':
                    Datalist[i]='0'
        if(Way=='date'):
            for j in range(1,(len(Datalist)/2+1)):
                Datalist.pop(j)
    writeLog(C.STARTSuccess,"tranData: ")
    return Datalist
class Source:
    def __init__(self,Url):
        self.Url=Url
        writeLog(C.STARTSuccess,Way='w')
    def Urldata(self,Way='GET',SQL=False,**kwargs):
        time.sleep(CONSTANT.TimeLimit)
        if (Way=='GET'):
            Req = urllib2.Request(self.Url,headers=CONSTANT.Headers)
            try:
                Text = urllib2.urlopen(Req).read()
            except UnicodeDecodeError as e:
                writeLog(C.UNICODEError,'%s'%self.Url)
                print('Please Try GzipSource_function')
                raise e
            except urllib2.URLError as e:
                writeLog(C.URLError,'%s'%self.Url)
                print("Please Try again")
                raise e
            except socket.error as e:
                writeLog(C.SOCKETError,'%s'%self.Url)
                raise e
            else:
                if(SQL):
                    try:
                        creatTable(C.SQLTable)
                    except:
                        writeLog(C.IOError,'%s --SQLCREACT'%self.Url)
                    finally:
                        addtoSome(C.SQLTable,Key=C.SQLURLName,Value=self.Url)
                        writeLog(C.SQLSuccess,'%s'%self.Url)
                writeLog(C.STARTSuccess,'%s'%self.Url)
                return Text
        elif(Way=='POST'):
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            PostData={'DCity':'%s'%tranName(kwargs['Departure']),'RCity':'%s'%tranName(kwargs['Destination']),'DDate':'%s'%kwargs['Date']}
            urllib2.install_opener(opener)
            try:
                PostData = urllib.urlencode(PostData)
                Request = urllib2.Request(self.Url, PostData, CONSTANT.Headers)  #(url,data=NONE,headers)
                Response = urllib2.urlopen(Request).read()
            except:
                writeLog(C.VALUEError,'%s'%self.Url)
                raise urllib2.URLError
            else:
                if(SQL):
                    try:
                        creatTable(C.SQLTable)
                    except:
                        writeLog(C.IOError,'%s --SQL'%self.Url)
                    finally:
                        addtoSome(C.SQLTable,Key=C.SQLURLName,Value=self.Url)
                        writeLog(C.SQLSuccess,' SQL: %s'%self.Url)
                        writeLog(C.STARTSuccess,' SQL: %s'%self.Url)
            writeLog(C.STARTSuccess,'%s'%self.Url)
            return Response
    def gzipSource(self):
        Req = urllib2.Request(self.Url,headers=CONSTANT.Headers)
        Text = urllib2.urlopen(Req).read()
        data = StringIO.StringIO(Text)
        gzipper = gzip.GzipFile(fileobj=data)
        html = gzipper.read()
        return html
    def repeatReq(self):
        while(CONSTANT.Attempts<3 and not CONSTANT.SUCCESS):
            try:
                writeLog(C.STARTSuccess,'%s'%self.Url)
                self.Urldata()
                CONSTANT.SUCCESS=True
            except:
                CONSTANT.Attempts+=1
                if CONSTANT.Attempts>CONSTANT.AttemptsMaxTime:
                    writeLog(C.STARTError,'%s'%self.Url)
    def useSelenium(self):
        try:
            Driver=webdriver.PhantomJS(executable_path="E:\PyGame\spider\phantomjs\phantomjs.exe")
        except AttributeError as e:
            writeLog(C.ATTRIBUTEError,Info="Selenium:%s "%self.Url)
        else:
            Driver.get(self.Url)
            writeLog(C.STARTSuccess,'%s'%self.Url)
            return Driver.page_source
if __name__ == '__main__':
    pass


