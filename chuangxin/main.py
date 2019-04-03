import base64
import hashlib
import json
import urllib.parse

import requests
from config import *
import re
username = '15281106'
password = 'wscjxky123'

def get_session(ssr):
    login_url='http://jwc.bjtu.edu.cn:82/LoginAjax.aspx?callback=jQuery172006346453567623689_1554310429909&' \
              'username=%s&password=%s&type=1&_=1554310449634'%(username,password)
    user_val=ssr.get(login_url).text
    id=re.search('LoginInUIA":"(.+)",',user_val).group(1)
    uid=re.search('UserName":"(.+)"',user_val).group(1)
    ver_url='http://jwc.bjtu.edu.cn/Admin/UserInfo/Login.aspx?' \
            'LoginInUI=%s&UserName=%s'%(urllib.parse.urlencode(id),uid)
    val_res=ssr.get(ver_url).text
    print(val_res)

    res=ssr.get('http://jwc.bjtu.edu.cn:82/Welcome.aspx')


    pass


def get_courses():
    data_dict = {
        'start': 0,
        'length': 100,
        'orgId': 'KY002',
        'isCanJoin': 1,
        'isSignUp': 0,
    }
    response = requests.post(base_url + 'credit/loadCreditChairList',
                             data=data_dict, headers=headers)
    course = json.loads(response.text)
    course_id = course['data'][0]['id']
    course_start_time = course['data'][0]['signUpStartDate']
    course_end_time = course['data'][0]['signUpEndDate']

    return course_id, course_start_time


def sign_courses(course_id):
    data_dict = {
        'ccId': course_id,
    }
    response = requests.post(base_url + 'credit/stuSignUpChairInfo',
                             data=data_dict, headers=headers)
    res_code = json.loads(response.text)['msg']
    if res_code == '3':
        print('时间未到')
    return res_code
if __name__ == '__main__':

    ssr = requests.session()
    ssr=get_session(ssr)
# course = get_courses()
# course_id, start_time = get_courses()
# result = sign_courses(course_id)
# print(result)
