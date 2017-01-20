import time

class CONSTANT:
    Headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    TimeLimit=3
    SUCCESS=False
    Attempts=0
    AttemptsMaxTime=5
    List=[]
    Str=''
    logfile='log.txt'
    Outfile='UrlList.txt'
    Imgstart=0

    SQLName='Data.db'
    SQLTable='Url'
    SQLURLSource='UrlSource'
    SQLURLName='Url'
    SQLIMGName='IMG'
    Dirname='Temp'
    ExcelName='Chart.xls'
    STARTError=000
    IOError=001
    INDEXError=002
    VALUEError=003
    SOCKETError=004
    UNICODEError=005
    URLError=006
    ATTRIBUTEError=007

    STARTSuccess=100
    URLSuccess=102
    SQLSuccess=103
    IOSuccess=101
def list_is_null(list):
        if( list == [] ):
            print('list is Null')
            return True
        return False
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str,str):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value
def to_str(unicode_or_str):
    if isinstance(unicode_or_str,str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value
def writeLog(LogNum,Info=' ',Way='a'):
    if Way=='w':
        File = open(CONSTANT.logfile,'w')
        File.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   ')
        if(LogNum==CONSTANT.STARTSuccess):
            File.write('The Spider Has Begun Successfully'+'\n')
        else:
            File.write('The Spider Has not Begun'+'\n')
        File.close()
    else:
        try:
            File = open(CONSTANT.logfile,'a')
            File.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   ')
            if(LogNum==CONSTANT.STARTSuccess):
                File.write('The Spider: %s Has Accomplished Successfully'%Info+'\n')
            elif(LogNum==CONSTANT.STARTError):
                File.write('The Spider: %s Is Failed to complete '%Info+'\n')
            elif(LogNum==CONSTANT.SQLSuccess):
                File.write('The %s Has Execute Successfully'%Info+'\n')
            elif(LogNum==CONSTANT.IOSuccess):
                File.write('The %s Has Save Successfully'%Info+'\n')
            elif(LogNum==CONSTANT.URLSuccess):
                File.write('The URL:%s Has Got Successfully'%Info+'\n')
            elif(LogNum==CONSTANT.VALUEError):
                File.write('The VALUE:%s Failed to Save '%Info+'\n')
            elif(LogNum==CONSTANT.INDEXError):
                File.write('The INDEX:%s Failed to Get '%Info+'\n')
            elif(LogNum==CONSTANT.IOError):
                File.write('The %s Failed to Input '%Info+'\n')
            elif(LogNum==CONSTANT.URLError):
                File.write('The URL:%s Failed to open '%Info+'\n')
            elif(LogNum==CONSTANT.UNICODEError):
                File.write('The URL:%s Failed to Code  '%Info+'\n')
            elif(LogNum==CONSTANT.ATTRIBUTEError):
                File.write('The %s Has No Attribute '%Info+'\n')
            else:
                File.write('The ERROR Can Not Found '+'\n')
        finally:
            File.close()
if __name__ == '__main__':
    pass
     # Test list_is_null function
     # a=[]
     # assert list_is_null(a) is True
     # Test writeLog function
     # with open('log.txt','w') as Test:
     #    Test.write("Test")
     #    assert Test is not None
