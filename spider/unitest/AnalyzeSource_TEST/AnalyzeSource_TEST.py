from spider.AnalyzeSource import *
URL='http://www.pop-fashion.com/'
'''test getUrllist function Way=link'''
# Source=Source(URL)
# Data=Source.Urldata()
# assert getUrllist(Data,Way='link') is not None

'''test getUrllist function Way=img'''';'
# Source=Source(URL)
# Data=Source.Urldata()
# assert getUrllist(Data,Way='img') is not None

'''test getTitlelist function Way=link'''
# Source=Source(URL)
# Data=Source.Urldata()
# assert getTitlelist(Data,Way='link') is not None

'''test getTitlelist function Way=img'''
Source=Source(URL)
Data=Source.Urldata()
assert getTitlelist(Data,Way='img') is not None