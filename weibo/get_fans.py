import requests
import json

import time
def get_fans():
    for page in range(11):
        data = requests.get('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'
                            '5477996247&luicode=10000011&lfid=1005055477996247&sudaref=login.sina.com.cn&since_id=%s' % page)
        with open('xixi_data_%s.json' % page, 'w') as f:
            f.write(json.dumps(data.json()))
        time.sleep(1)
def get_followers():
    for page in range(14):
        data = requests.get('https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_3'
                            '291944305&luicode=10000011&lfid=1005053291944305&page=%s' % page)
        with open('liang_data_%s.json' % page, 'w') as f:
            f.write(json.dumps(data.json()))
        time.sleep(1)
# get_followers()
for page in range(2,14):
    try:
        with open('xixi_data_%s.json' % page, 'r')as f:
            data = json.loads(f.read())
            cards=data['data']['cards'][0]['card_group']
            for card in cards:
                user_name=(card['user']['screen_name'])
                print(user_name)
    except:
        pass
