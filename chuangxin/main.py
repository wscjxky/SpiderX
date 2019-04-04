import base64
import hashlib
import json
import urllib.parse

import requests
from config import *
import re

username = '15281106'
password = 'wscjxky123'
course_name = '产业互联网浪潮下的产品创新'
orgId = 'KY002'
length = 5


def get_session(ssr):
    login_url = 'http://jwc.bjtu.edu.cn:82/LoginAjax.aspx?callback=jQuery172006346453567623689_1554310429909&' \
                'username=%s&password=%s&type=1&_=1554310449634' % (username, password)
    ssr_url = 'http://jwc.bjtu.edu.cn:82/NoMasterJumpPage.aspx?URL=jwcJybs&FPC=page:jwcJybs'
    locate_url = 'http://202.112.159.147/getIndexPage'
    user_val = ssr.get(login_url).text
    id = re.search('LoginInUIA":"(.+)",', user_val).group(1)
    uid = re.search('UserName":"(.+)"', user_val).group(1)
    ver_url = 'http://jwc.bjtu.edu.cn/Admin/UserInfo/Login.aspx?LoginInUIA=%s&UserName=%s&LoginFor=' % (id, uid)
    ssr.get(ver_url).text
    ssr.get(ssr_url).text
    ssr.get(locate_url).text
    session = dict(ssr.cookies)['SESSION']
    print(session)
    return session


def get_courses(session):
    data_dict = {
        'start': 0,
        'length': length,
        'orgId': '%s' % orgId,
        "ccName": "%s" % course_name,
        'isCanJoin': '',
        'isSignUp': 0,
    }
    headers['Cookie'] = 'SESSION=%s' % session
    response = requests.post(base_url + 'credit/loadCreditChairList',
                             data=data_dict, headers=headers)
    print(response.text)
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
        print('报名时间未到')
    elif res_code == '4':
        print('报名时间已结束')
    return res_code


if __name__ == '__main__':
    ssr = requests.session()
    session = get_session(ssr)
    course_id, start_time = get_courses(session)
    result = sign_courses(course_id)
