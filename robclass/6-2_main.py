import re
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
import json
import requests
from selenium.webdriver.chrome.options import Options

from chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('wscjxky', 'wscjxky123', '898146')  # 用户中心>>软件ID 生成一个替换 96001
from config import FateadmApi, robclass_headers, headers, headers_image, check_classheader

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
    url = 'https://mis.bjtu.edu.cn/home/'
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element_by_css_selector('#id_loginname')
    elem.send_keys(username)
    elem = driver.find_element_by_xpath('//*[@id="id_password"]')
    elem.send_keys(password)
    elem = driver.find_element_by_xpath('//*[@id="login"]/dl/dd[2]/div/div[3]/button')
    elem.click()
    elem = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[6]/div/div/h5/a')
    elem.click()
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
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
        post_request(cookies, class_code, hashkey, answer, req_id, pred_type, 50)
    re = re.headers['Set-Cookie']
    message = re[re.find('[['):re.find(']]') + 2]
    res = str(json.loads(eval("'" + message + "'")))
    print(res)
    if "选课成功" in res:
        return 200
    elif "课堂无课余量" in res:
        return 404
    elif "验证码" in res:
        if pred_type == 'pp':
            api.Justice(req_id)
        else:
            res = chaojiying.ReportError(req_id)
            print(res)
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
    # sess=HTMLSession()
    # res=sess.get(check_url, cookies=cookies, headers=check_classheader)
    # print(res.text)
    res = requests.get(check_url, cookies=cookies, headers=check_classheader,
                       proxies={"http": "http://{}".format(proxy)}
                       )
    if res.status_code == 503:
        # proxy = get_proxy()
        # delete_proxy(proxy)
        # print('换ip：%s' % proxy)
        time.sleep(1)
        error_503 += 1
        print(error_503)
        if error_503 % 30 == 0:
            print(error_503)
            # print(503)
            # is_free(kecheng_code, xuhao, proxy=proxy, pred_type=pred_type)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('div', id='container')
    if table:
        class_trs = table.find_all('tr')[1:]
        for tr in class_trs:
            for index_kecheng, k_code in enumerate(kecheng_code):
                if k_code in tr.text:
                    has_free = tr.find('input')
                    if has_free:
                        ok = False
                        class_code = has_free["value"].strip()
                        class_name = tr.find('div', class_='ellipsis').text.strip()
                        class_name = re.search("】(.*)", class_name).group(1)

                        if xuhao[index_kecheng] in class_name:
                            ok = True
                        else:
                            class_name = tr.find('div', class_='hide').text.strip()
                            class_name = re.search("】(.*)", class_name).group(1)
                            if xuhao[index_kecheng] in class_name:
                                ok = True
                        if ok:
                            print("有课余量：")
                            print(class_name)
                            print(class_code)
                            res = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/', cookies=cookies,
                                               headers=headers_image)
                            json_data = res.json()
                            hashkey = json_data['key']
                            print(json_data)
                            img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'],
                                                    headers=headers)
                            if pred_type == 'pp':
                                pred_type = 'pp'
                                answer, req_id = api.Predict(40300, img_data.content)
                            else:
                                pred_type = 'cjy'
                                answer, req_id = chaojiying.PostPic(img_data.content, 2003)
                            result = post_request(cookies=cookies, class_code=class_code, hashkey=hashkey,
                                                  answer=answer,
                                                  req_id=req_id, pred_type=pred_type)
                            if result == 200:
                                return True
    return False


if __name__ == '__main__':
    with open('rob_data.txt', 'r', encoding='utf8')as f:
        ls = f.readlines()
        for line in ls:
            if line != '':
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
        try:
            time.sleep(time_delay)
            if retry_num > retry_max:
                reset = True
                retry_num = 0
                # cookies = get_Session()
                continue
            if i == len(kecheng_code):
                i = 0
            if is_free(kecheng_code=kecheng_code, xuhao=xuhao, pred_type='cjy'):
                print(username, password)
                print("搶課完成" + str(kecheng_code[i]))
                break
            else:
                if retry_num % 20 == 0:
                    print('retry_time : ' + str(retry_num))
                i += 1
                retry_num += 1
                reset = False
        except Exception as e:
            # raise (e)
            print(e)
            continue
