# -*- coding: utf-8 -*- #用于显示中文
from spider.getSource import *
POSTURL='http://www.syuntravel.cn/PassengerTicket/SearchHistoryTicket'
GETURL='http://www.baidu.com/'

'''Test urlData function Way==POST'''
# Source=Source(POSTURL)
# Data=Source.Urldata(Way='POST',Departure='北京',Destination='上海',Date='2016-10')
# assert Data is not None

'''Test urlData function Way==GET'''
# Source=Source('http://www.meishichina.com/')
# assert Source.Urldata() is not None

'''Test urlData functiong SQL==True Way==GET'''
# Source=Source(GETURL)
# Data=Source.Urldata(SQL=True)
# assert DATA is not None

'''Test urlData function SQL==True Way==POST'''
# Source=Source(POSTURL)
# Data=Source.Urldata(SQL=True,Way='POST',Departure='北京',Destination='上海',Date='2016-10')
# assert Data is not None

'''Test useSelenium function'''
# Source=Source(GETURL)
# assert Source.useSelenium() is not None


'''Test gzipSource function'''
# Source=Source('http://www.xesvmh.cc')
# Data=Source.Urldata()
# print(Data)
# Source=Source('http://www.xesvmh.cc')
# Data=Source.gzipSource()
# print(Data)