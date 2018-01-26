# -*- coding: utf-8 -*- #

import sqlite3
tablename='sentence'
def creatTable(tablename):
    conn = sqlite3.connect('DATA.db')
    try:
        conn.execute('''CREATE TABLE %s (
    id      INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL,
    dynasty CHAR    NOT NULL,
    writer  CHAR    NOT NULL,
    word    TEXT    NOT NULL
);''' % tablename)
    except:
        conn.close()
        return
def execute(sql):
    conn = sqlite3.connect('DATA.db')
    conn.execute(sql)
    conn.commit()
    conn.close()

def getDatafromsql(tablename,sql=''):
    try:
        if(sql):
            sql=sql
        else:
            sql = '''SELECT * FROM %s ''' % (tablename)
        conn = sqlite3.connect('DATA.db')
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception,e:
        print e
        return False
def addData(tablename,dict):
    sql='INSERT INTO %s('%tablename
    for key in dict:
        sql+=str(key)+','
    sql=sql.strip(',')
    sql+=')VALUES ('
    for key,value in dict.items():
        sql += "'"+value.encode('utf8') + "',"
    sql = sql.strip(',')
    sql+=')'
    try:
        execute(sql)
        return True
    except Exception,e :
        return False

def selectData(tablename, data):
    try:
        sql = '''SELECT id FROM %s where word==('%s')''' % (tablename, data)
        conn = sqlite3.connect('DATA.db')
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchone()
        cur.close()
        conn.close()
        return int(results[0])
    except:
        return False
# if __name__ == '__main__':
#     addData('s','s','s')
#     creatTable(tablename)
#     addData(tablename,'a','s','''知我者，谓我心忧；不知我者，谓我何求。


def findData(tablename,dic):
    sql = 'SELECT * FROM %s where ' % tablename

    for key, value in dic.items():
        try:
            value=str(value)
            value = value.encode('utf8')
        except Exception,e:
            print e
            pass
        sql += key +"=="+"'" + value + "'and"
    sql=sql[:-3]
    conn = sqlite3.connect('DATA.db')
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchone()
    cur.close()
    conn.close()
    return results
