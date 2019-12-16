from config import FateadmApi, robclass_headers, headers, headers_image, get_user_agent
import datetime
import re
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
import json
import requests
from selenium.webdriver.chrome.options import Options
import os

from chaojiying import Chaojiying_Client
from chaoren import *
from YDM import *

sleep_time_503 = 2
chaoren_client = Chaoren()
chaoren_client.data['username'] = 'wscjxky'  # 修改为打码账号
chaoren_client.data['password'] = 'wscjxky123'  # 修改为打码密码
chaojiying = Chaojiying_Client(
    'wscjxky', 'wscjxky123', '898146')  # 用户中心>>软件ID 生成一个替换 96001

pd_id = "103797"
pd_key = "L5oPz3M0cbHJhiOfzs1gTk4oW9b2yVsB"
app_id = "303997"  # 开发者分成用的账号，在开发者中心可以查询到
app_key = "o8SL2OUcncoCeYCDuN7PhS/54Ns/wepQ"
pred_type = "40300"
api = FateadmApi(app_id, app_key, pd_id, pd_key)


def get_Session():
    BCOOKIES = {}
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Chrome(executable_path='chromedriver',
                    options=chrome_options)
    url = 'http://jwc.bjtu.edu.cn'
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element_by_xpath(
        '/html/body/div[3]/table/tbody/tr[1]/td[1]/div/div[1]/span/a[1]')
    elem.click()
    time.sleep(0.8)
    elem = driver.find_element_by_xpath('//*[@id="TextBoxUserName"]')
    elem.send_keys(username)
    elem = driver.find_element_by_xpath('//*[@id="TextBoxPassword"]')
    elem.send_keys(password)
    elem = driver.find_element_by_xpath('//*[@id="rbUserCenter"]')
    elem.click()
    elem = driver.find_element_by_xpath(
        '//*[@id="ButtonLogin"]')
    elem.click()
    time.sleep(1)

    elem = driver.find_element_by_xpath(
        '//*[@id="ctl00_ctl00_ctl00_ctl00_placeHolderContent_placeHolderContent_placeHolderMenuBar_navMenu_tvNavMenut0"]')
    elem.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    # time.sleep(10)
    cookie = driver.get_cookies()
    # time.sleep(1)
    assert len(cookie) == 2
    # while len(cookie) <= 1:
    #     time.sleep(2)
    #     get_Session()
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
    print('reload' + str(BCOOKIES))

    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
    driver.close()
    driver.quit()
    return ssrequest.cookies


# from requests_html import HTMLSession

def post_request(cookies, class_code, hashkey, answer, req_id, pred_type='pp', count=0):
    # while count < 50:
    #     check_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page=1&perpage=500'
    #     res = requests.get(check_url, cookies=cookies, headers=check_classheader)
    #     count += 1
    data = {'checkboxs': class_code,
            # 'is_cross':True
            'hashkey': hashkey,
            'answer': answer
            }
    re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       cookies=cookies,
                       headers=robclass_headers,
                       allow_redirects=False,
                       data=data)
    if re.status_code == 503:
        print(re.status_code)
        print("重新提交抢课请求")
        time.sleep(0.3)
        post_request(cookies, class_code, hashkey,
                     answer, req_id, pred_type, 50)
    print(re)
    re = re.headers['Set-Cookie']
    message = re[re.find('[['):re.find(']]') + 2]
    res = str(json.loads(eval("'" + message + "'")))
    print(pred_type + res)
    if "选课成功" in res:
        return 200
    elif "课堂无课余量" in res:
        return 404
    elif "验证码" in res:
        if pred_type == 'pp':
            api.Justice(req_id)
        elif pred_type == 'cjy':
            res = chaojiying.ReportError(req_id)
        elif pred_type == 'ydm':
            res = YDMHttp.report(req_id)
        else:
            chaoren_client.report_err(req_id)
        return 403
    else:
        return 500


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content.decode('utf8')


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def is_free(kecheng_code, xuhao, proxy='', pred_type='pp'):
    global cookies, error_503
    check_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page=1&perpage=500'
    res = requests.get(check_url, cookies=cookies, headers=get_user_agent(),
                       proxies={"http": "http://{}".format(proxy)}
                       )
    if res.status_code == 503:
        # proxy = get_proxy()
        # delete_proxy(proxy)
        # print('换ip：%s' % proxy)
        time.sleep(sleep_time_503)
        error_503 += 1
        if error_503 % 30 == 0:
            print(f"503次数:{error_503}")
            print(error_503)
            # print(503)
            # is_free(kecheng_code, xuhao, proxy=proxy, pred_type=pred_type)

    res = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/', cookies=cookies,
                       headers=headers_image)
    json_data = res.json()
    hashkey = json_data['key']
    img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'],
                            headers=headers)
    print(img_data.content)
    # answer, req_id = api.Predict(40300, img_data.content)
    yundama = YDMHttp()
    req_id, answer = yundama.decode(img_data.content, 2003, 15)
    print(answer)
    result = post_request(cookies=cookies, class_code=93205, hashkey=hashkey,
                            answer=answer,
                            req_id=req_id, pred_type='ydm')



if __name__ == '__main__':
    with open('rob_data.txt', 'r', encoding='utf8')as f:
        ls = f.readlines()
        for line in ls:
            if line != '' and "#" not in line:
                line = line.strip('\n')
                data = line.split(' ')
                username = data[0]
                password = data[1]
                kecheng_code = data[2].split(',')
                xuhao = data[3].split(',')
                name = data[4].split(',')

    assert len(kecheng_code) == len(xuhao)
    print(len(kecheng_code), len(xuhao))
    print(username, password, kecheng_code, xuhao, name)
    # username = '18251076'
    # password = '10962905'
    # kecheng_code = ['85L074T']
    # xuhao = ["11"]
    error_503 = 0
    time_delay = 0.2
    retry_max = 50000
    reset = False
    i = 0
    retry_num = 0
    cookies = get_Session()
    while True:
        # try:
            time.sleep(0.5)
            if is_free(kecheng_code=kecheng_code, xuhao=xuhao, pred_type='pp'):
                print(username, password)
                print("搶課完成" + str(kecheng_code[i]))
                break
            else:
                if retry_num % 20 == 0:
                    print(name[0] + " " + str(time.strftime("%H:%M:%S")
                                              ) + '  retry_time : ' + str(retry_num))
                i += 1
                retry_num += 1
                reset = False
        # except Exception as e:
        #     raise (e)
        #     print(e)
        #     continue
