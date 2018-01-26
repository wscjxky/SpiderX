# -*- coding:utf8 -*-
from time import time
import sqlite3
import jieba
import re
import numpy as np
import matplotlib.pyplot as plt
from sentence.constant import *
from sentence.sql import *

stopwords = open(STOPWORDS_FILE, 'r').read().splitlines()
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '|', '@', '#', '&', '\\', '%', '$', '*', '=',
                        '\\n', '\n', 'abstract=', '{', '}']



# seg_list = jieba.lcut("我来到.北京m清华大学,")
# for i in seg_list:
#     print(i)

def createDict():
    results = getDatafromsql(SENTENCE_TABLE_name)
    for row in results:
        text=row[3]
        dynasty=row[2]
        writer=row[1]
        seg_list = jieba.lcut(text,cut_all=True)
        for word in seg_list:
            if not word in english_punctuations:
                if word.encode('utf8') not in stopwords:
                    if  word:
                        print dynasty
                        dic={'dynasty':dynasty,'writer':writer,'word':word}
                        print dic
                        addData(DICT_TABLE_name,dic)
def setFile(dyn):
    results = getDatafromsql(SENTENCE_TABLE_name,'''SELECT * FROM %s WHERE `dynasty`=='%s'
    ''' % (SENTENCE_TABLE_name,dyn))

    with open((dyn+'.txt').decode('utf8'),'a+') as f :
        for row in results:
            text=row[3]
            f.write(text.strip('').encode('utf-8'))
def getWordRate(dyn):
    num=0
    file_nparr = np.zeros((10, 15300))
    with open((dyn+'.txt').decode('utf8'), 'r') as f:
        lines=f.readlines()
        for l in lines:
            seg_list = jieba.lcut(l, cut_all=True)
            for word in seg_list:
                if not word in english_punctuations:
                    if word.encode('utf8') not in stopwords:
                        if word:
                            num += 1
                            id=selectData(DICT_TABLE_name,word)
                            if (id):
                                file_nparr[0][id]+=1
    np.save(TEMP_NPY,file_nparr)
def getWordTop():
    nparr= np.load(TEMP_NPY)
    import redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    for key,value in enumerate(nparr[0]):
        if value>35:

            r.hset('top',findData(DICT_TABLE_name, {'id': key})[3],value)
            print value
            print findData(DICT_TABLE_name, {'id': key})[3]
def plot(narray):
    np.set_printoptions(threshold='nan')
    plt.imshow(narray)
    plt.show()

# createDict()
dyn='隋唐五代'
# setFile(dyn)
getWordRate(dyn)
getWordTop()

# a='s'
# d={'dynasty':a,'writer':'sd','word':'sdf'}

#
# print addData(SENTENCE_TABLE_name,d)
# creatTable(DICT_TABLE_name)
