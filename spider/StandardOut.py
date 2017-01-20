# -*- coding: utf-8 -*- #用于显示中文
import os
import xlsxwriter
from AnalyzeSource import *
from config import CONSTANT as C, writeLog
import socket
import threading
class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func
    def run(self):
        apply(self.func, self.args)
def downloadImg(Imgnum,Urllist,Thread=False):
    if os.path.exists(C.Dirname)==False:
        os.mkdir(C.Dirname)
        writeLog(C.STARTSuccess,'Dir:%s '%C.Dirname)
    if(Thread):
        byThread(Imgnum,Urllist)
    else:
        writeLog(C.STARTSuccess,'Dir:%s '%C.Dirname)
        for Url in Urllist:
            SUCCESS=False
            Attempts=0
            AttemptsMAX=C.AttemptsMaxTime
            Imgtype=Url[-3:]
            if(Imgtype=='jpg' or Imgtype=='png'):
                while(SUCCESS==False and Attempts<AttemptsMAX):
                    try:
                        Request = urllib2.Request(Url)
                        Request.add_header('Referer','http://www.baidu.com')
                        Request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
                        Response = urllib2.urlopen(Request)
                        Data = Response.read()
                        writeLog(C.URLSuccess,'%s '%Url)
                    except ValueError:
                        writeLog(C.VALUEError,'Url Need Add The Main website: %s'%Url)
                        Attempts+=1
                        continue
                    except urllib2.URLError as e:
                        Imgnum+=1
                        Attempts+=1
                        writeLog(C.URLError,'IMG: %s'%Url)
                        continue
                    except socket.timeout as e:
                        Attempts+=1
                        Imgnum+=1
                        writeLog(C.SOCKETError,'IMG: %s Please Try byThread function'%Url)
                        continue
                    else:
                        SUCCESS=True
                        File = open("%s/%s.%s" % (C.Dirname,str(Imgnum),Imgtype),"wb")
                        File.write(Data)
                        Imgnum+=1
                        writeLog(C.IOSuccess,'IMG: %s'%Url)
                        File.close()
def byThread(Imgnum,Urllist):
    def downImg(Imgnum,Url):
        try:
            Imgtype=Url[-3:]
            Request = urllib2.Request(Url)
            Request.add_header('Referer','http://www.baidu.com')
            Request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
            Response = urllib2.urlopen(Request)
            Data = Response.read()
            File = open("%s/%s.%s" % (C.Dirname,str(Imgnum),Imgtype),"wb")
            File.write(Data)
        except:
            writeLog(C.STARTError,"Img : %d " %Imgnum)
            print('%d is failed to download'%Imgnum)
    if os.path.exists(C.Dirname)==False:
        os.mkdir(C.Dirname)
        writeLog(C.STARTSuccess,'Dir:%s '%C.Dirname)
    Threadlist=[]
    try:
        for Url,Imgnum in zip(Urllist,range(len(Urllist))):
            Threadlist.append(MyThread(downImg,(Imgnum,Url,)))
        for t in Threadlist:
            t.setDaemon(True)  #如果你在for循环里用，不行， 因为上一个多线程还没结束又开始下一个
            t.start()
            writeLog(C.STARTSuccess,' %s ' %t)
        for j in Threadlist:
            j.join()
        writeLog(C.STARTSuccess,'Thread Download %s '% C.Dirname)
    except:
        writeLog(C.ATTRIBUTEError,'THE Thread: %s ' %C.Dirname)
def writeExcel(Filename,Data):
    Datalist=tranData(Data)
    Datalist1=tranData(Data,Way='price')
    print(Datalist)
    print(Datalist1)
    try:
        workbook = xlsxwriter.Workbook(Filename)
        worksheet=workbook.add_worksheet()
    except IOError as e:
        writeLog(C.IOError,'Excel:')
    except NameError as e:
        writeLog(C.VALUEError,'Excel:')
    else:
        try:
            worksheet.write_column('A1',Datalist)
            worksheet.write_column('B1',map(int,Datalist1))
            chart = workbook.add_chart({'type': 'line'})
            chart.add_series({'values': '=Sheet1!$B$1:$B$30'})
            worksheet.insert_chart('F1', chart)
        except AttributeError as e:
            writeLog(C.ATTRIBUTEError,'Excel: %s '%Filename)
        except UnicodeError as e:
            writeLog(C.UNICODEError,'Excel: %s '%Filename)
        except IOError as e:
            writeLog(C.IOError,'Excel: %s '%Filename)
        except ValueError as e:
            writeLog(C.VALUEError,"Excel : %s "%Filename)
    finally:
        workbook.close()
        writeLog(C.STARTSuccess,'Excel: %s '%Filename)
if __name__ == '__main__':
    pass
    Source=Source('https://www.mmonly.cc/')
    Data=Source.gzipSource()
    imglist=getUrllist(Data,Way='img')
    print(imglist)
    # imglist=['http://img.ivsky.com/img/tupian/m/201407/25/kalajun-002.jpg']
    downloadImg(C.Imgstart,imglist)
    # Test writeExcel function
    # url='http://www.syuntravel.cn/PassengerTicket/SearchHistoryTicket'
    # Source=Source(url)
    # Data=Source.Urldata(Way='POST',Departure='北京',Destination='上海',Date='2016-10')
    # writeExcel('a.xls',Data)