# -*- coding: utf-8 -*- #用于显示中文
from spider.StandardOut import*
'''Test downloadImg function '''

# Source=Source('https://www.mmonly.cc/')
# Data=Source.gzipSource()
# imglist=getUrllist(Data,Way='img')
# downloadImg(C.Imgstart,imglist)

'''Test downloadImg function Thread=True'''
# Source=Source('http://wmtp.net/')
# Data=Source.Urldata()
# imglist=getUrllist(Data,Way='img')
# downloadImg(C.Imgstart,imglist,Thread=True)

'''Test writeExcel function'''
url='http://www.syuntravel.cn/PassengerTicket/SearchHistoryTicket'
# Source=Source(url)
# Data=Source.Urldata(Way='POST',Departure='北京',Destination='上海',Date='2016-11')
# writeExcel(C.ExcelName,Data)