from nosql import DB
# DB.sunionstore('co_ori_users','co_users')
keys=DB.keys('*:combine:*')
for i in keys:
    DB.delete(i)