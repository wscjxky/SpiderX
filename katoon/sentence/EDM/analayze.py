# -*- coding: utf-8 -*- #
import urllib2
import re
from nosql import DB
from constant import *
from bs4 import BeautifulSoup
from MAIN import del_cache
# b=[432271872,492496544,551951796]
# ori_id=264257752
# a='user:108549140:like_song'
# ori_name='user:264257752:top_songs'
# SOURCE_STRINGS=''
# NODE_STRINGS=''
def inter_user_likesongs():
    userlist=DB.lrange('user',0,200)
    for i in userlist:
        for j in userlist:
            if j!=i:
                ori_tname='user:'+str(i)+':like_songs'
                com_tname='user:'+str(j)+':like_songs'
                DB.sinterstore('combine:ouser:'+str(i)+':cuser:'+str(j),ori_tname,com_tname)
                print i,j

def get_user_name_db(user_id):
    return DB.hget('user:'+str(user_id),'name')
def del_u(string):
    string=  re.sub(r"u'", "'", str(string))
    return re.sub(r"'target'", "target", (string))

def get_user_relation(ori_id):
    global SOURCE_STRINGS
    global NODE_STRINGS
    global ITER_TIMES
    combine_user_list=[]
    keys=DB.keys()
    ori_user_name=get_user_name_db(ori_id)
    ori_table_name='combine:ouser:'+str(ori_id)+':cuser:'
    if ori_user_name:
        node = {
            'category': '人物'.decode('utf-8') ,
            'name': ori_user_name.decode('utf-8'),
            'value': 100
        }
        #去掉u,替换掉u'的u，而不去掉\uex的u
        NODE_STRINGS+=del_u(node)+','
    for key in keys:
        if  ori_table_name in key:
            print key
            value=DB.scard(key)
            cuser_id =re.search(r':cuser:(\d+)$',key)
            cuser_id = cuser_id.group(1)
            combine_user_list.append(cuser_id)

            user_name=get_user_name_db(cuser_id)
            if user_name and ori_user_name:
                node = {
                    'category': '人物'.decode('utf-8'),
                    'name': user_name.decode('utf-8'),
                    'value': value
                }
                NODE_STRINGS += del_u(node) + ','
                source = {
                    'source': ori_user_name.decode('utf-8'),
                    'target': user_name.decode('utf-8') ,
                    'weight': value
                }
                SOURCE_STRINGS+=del_u(source)+','


    return combine_user_list

# combine_user_list=get_user_relation(ori_id)
# # 获取其他人的关系
# for cuser in combine_user_list[:5]:
#     get_user_relation(cuser)
# with open('temp.html','w')as f:
#     f.write((HTML_HEAD+NODE_STRINGS+HTML_MIDDLE+SOURCE_STRINGS+HTML_END))

# 人物
# combine:ouser:264257752:cuser:551951796
# 4950232


s = """
     阿萨德en: expression is a powerful tool for manipulating text.

    """.decode('utf8')
s='弟みたいな存在'.decode('utf8')
re_chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
re_korean_words=re.compile(u"[\uac00-\ud7ff]+")
re_janpan1_words = re.compile(u"[\u30a0-\u30ff]+")
re_janpan2_words = re.compile(u"[\u3040-\u309f]+")
re_english_words=re.compile(r"[\w]+")
# if re_janpan2_words.search(s, 0):
#     print re_janpan2_words.search(s, 0).group(0)
ENGLISH=0
KOREAN=0
CHINESE=0
JANPAN=0
songs_list=DB.smembers('songs')
for i in songs_list:
    name=DB.hget('songs:'+str(i),'name')
    if name:
        name=name.decode('utf8')
        print name
        if re_janpan2_words.search(name, 0):
            JANPAN += 1
            print JANPAN
            continue
        elif re_janpan1_words.search(name, 0):
            JANPAN += 1
            continue
        elif re_korean_words.search(name, 0):
            KOREAN += 1
            continue
        elif re_english_words.search(name, 0):
            ENGLISH += 1
            continue
        else:
            CHINESE += 1
            continue
print ENGLISH,KOREAN,CHINESE,JANPAN,
# E8586 K100 C1027 J893