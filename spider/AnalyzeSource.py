# -*- coding: utf-8 -*- #用于显示中文
from getSource import *
from config import CONSTANT,list_is_null
from config import to_str,to_unicode
from bs4 import BeautifulSoup


""""""
def getUrllist(Data,Way='link'):
    Soup=BeautifulSoup(Data,'html.parser')
    Linklist=CONSTANT.List
    with open('%s'%CONSTANT.Outfile,'w') as ListData:
        if(Way=='img'):
            Tag=Soup.find_all('img')
            for Link in Tag:
                CONSTANT.List.append(Link.get('src'))
                try:
                    ListData.write(Link.get('src')+'\n')
                except TypeError:
                    writeLog(C.IOError,'link: ')
                    pass
            if not(list_is_null(Linklist)):
                writeLog(C.STARTSuccess,"img: ")
                return Linklist
            else:
                writeLog(C.INDEXError,"img: ")
        if(Way=='link'):
            Tag=Soup.find_all('a',target=True)
            for Link in Tag:
                Linklist.append(Link.get('href'))
                ListData.write(Link.get('href')+'\n')
            if not(list_is_null(Linklist)):
                writeLog(C.STARTSuccess,"img: ")
                return Linklist
            else:
                writeLog(C.INDEXError,"img: ")
def getTitlelist(Data,Way='link'):
    Soup=BeautifulSoup(Data,'html.parser')
    Stringlist=CONSTANT.List
    with open('%s'%CONSTANT.Outfile,'w') as ListData:
        if('link' in Way):
            Tag=Soup.find_all('a',target=True)
            for Strings in Tag:         #Strings.get('title')
                for Str in Strings:
                    Stringlist.append(Str)
                    ListData.write(Str+'\n')
            if not(list_is_null(Stringlist)):
                writeLog(C.STARTError,"Stringlist: ")
                return Stringlist
            else:
                writeLog(C.INDEXError,"Stringlist:  ")
        if('img' in Way):
            Tag=Soup.find_all('img')
            for Strings in Tag:
                Stringlist.append(Strings.get('alt'))
                ListData.write(Strings.get('alt')+'\n')
            if not(list_is_null(Stringlist)):
                writeLog(C.STARTError,"Stringlist: ")
                return Stringlist
            else:
                writeLog(C.INDEXError,"Stringlist:  ")
if __name__ == '__main__':
    pass
    #test getUrllist
    # Source=Source('http://www.pop-fashion.com/')
    # Data=Source.Urldata()
    # assert getUrllist(Data,Way='link') is not None
    # assert getUrllist(Data,Way='img') is not None
    # Source=Source('http://www.pop-fashion.com/')
    # Data=Source.Urldata()
    # assert getTitlelist(Data,Way='link') is not None
    # assert getTitlelist(Data,Way='img') is not None

