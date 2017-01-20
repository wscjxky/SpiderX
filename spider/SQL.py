# -*- coding:utf-8 -*-
import sqlite3
from config import CONSTANT as C,writeLog
def creatTable(tablename):
    conn = sqlite3.connect('DATA.db')
    conn.execute('''CREATE TABLE %s
        (ID            INTEGER      PRIMARY KEY    AUTOINCREMENT  NOT NULL);''' % tablename)
    conn.close()
def execute(sql):
    conn = sqlite3.connect('DATA.db')
    conn.execute(sql)
    conn.commit()
    conn.close()
def delTable(tablename,id=0,all=True):
    if (all):
        sql='''DELETE FROM %s WHERE ID >= 1 ;'''%tablename
        execute(sql)
        sql='''UPDATE sqlite_sequence SET seq = 0 WHERE name = '%s';'''%tablename
        execute(sql)
    sql='''DELETE FROM %s WHERE ID = %d;''' % (tablename,id)
    execute(sql)
def addtoSome(tablename,Key,Value):
    try:
        addSegment(tablename,Key)
    except:
        writeLog(C.IOError,'Table:%s Has Exist'%tablename)
    finally:
        sql = '''INSERT INTO %s ('%s')
                VALUES ('%s')''' % (tablename,Key,Value)
        execute(sql)
def addtoItem(tablename,name):

    sql = '''INSERT INTO %s (NAME)
            VALUES ('%s')''' % (tablename,name)  #sql语句里也要‘’因为name传进去没有""
    execute(sql)
def addtoSegment(tablename,segmeng,data,ID):
    sql='''update %s set "%s"="%s" where ID=%d;''' % (tablename,segmeng,data,ID)
    execute(sql)
def selectId(tablename,id):
    sql ='''SELECT * FROM %s
            WHERE ID = %d''' % (tablename,id)
    conn = sqlite3.connect('DATA.db')
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchone()  #与all区别
    cur.close()
    conn.close()
    return results
def toZero():
    sql = '''DELETE FROM sqlite_sequence;'''
    execute(sql)
def addSegment(tablename,segname):
    sql='''ALTER TABLE %s ADD "%s" TEXT''' % (tablename,segname)
    execute(sql)
def copySegment(Tablename):
    sql='''CREATE TABLE TEMPTABLE
        (ID            INTEGER      PRIMARY KEY    AUTOINCREMENT  NOT NULL,
        NAME           TEXT    NOT NULL);
        insert into TEMPTABLE(ID,NAME) select ID,NAME from %s;
    '''% (Tablename)
if __name__ == '__main__':
    addtoSome('Url','imgurl','http://ww.vaisdujaskdh.com')
    addtoSome('Url','imgurl','http://ww.vaisdujassdfkdh.com')
    delTable('Url')
    addtoSome('Url','imgurl','http://ww.vaisdujaskdh.com')
