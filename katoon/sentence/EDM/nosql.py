# -*- coding:utf8 -*-

import redis

DB = redis.Redis(host='47.94.251.202', port=6379,db=10,password='wscjxky123')

# if __name__ == '__main__':
#
#     for i in range(5):  # 将需爬取的糗事百科前20页的url并存入urls集合
#         url = 'http://www.qiushibaike.com/hot/page/%d/' % (i + 1)
#         a='砸烂'.decode('utf8')
#         print DB.sadd(a, url) # 将url插入关键字urls集合中，若url已存在则不再插入
