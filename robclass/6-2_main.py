import re
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
import json
import requests
from selenium.webdriver.chrome.options import Options

from robclass.config import FateadmApi, robclass_headers, headers, headers_image, check_classheader

pd_id = "103797"  # 用户信息页可以查询到pd信息
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
    driver = Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    url = 'https://mis.bjtu.edu.cn/home/'
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element_by_css_selector('#id_loginname')
    elem.send_keys(username)
    elem = driver.find_element_by_xpath('//*[@id="id_password"]')
    elem.send_keys(password)
    elem = driver.find_element_by_xpath('//*[@id="form1"]/div/div/button')
    elem.click()
    elem = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[1]/td[6]/div/div/h5/a')
    elem.click()
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    cookie = driver.get_cookies()
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
    print('reload' + str(BCOOKIES))
    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
    driver.close()
    driver.quit()
    return ssrequest.cookies


# from requests_html import HTMLSession

def test_post():
    cookies = get_Session()
    hashkey, answer, req_id = getCode(cookies)
    data = {'checkboxs': 90177,
            'hashkey': hashkey,
            'answer': answer
            }
    result = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                           cookies=cookies,
                           headers=robclass_headers,
                           allow_redirects=False,
                           data=data)
    result = result.headers['Set-Cookie']
    message = result[result.find('[['):result.find(']]') + 2]
    res = str(json.loads(eval("'" + message + "'")))
    print(res)
    if "选课成功" in res:
        return 200
    elif "课堂无课余量" in res:
        return 404
    elif "验证码" in res:
        api.Justice(req_id)
        return 403

    else:
        return 500


def getCode(cookies):
    re = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/',
                      cookies=cookies,
                      headers=headers_image,
                      )
    json_data = re.json()
    hashkey = json_data['key']
    print(json_data)
    img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'], headers=headers)
    answer, req_id = api.Predict(pred_type, img_data.content)
    return hashkey, answer, req_id


def post_request(cookies, class_code, hashkey, answer, req_id):
    data = {'checkboxs': class_code,
            'hashkey': hashkey,
            'answer': answer
            }
    re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       cookies=cookies,
                       headers=robclass_headers,
                       allow_redirects=False,
                       data=data)
    re = re.headers['Set-Cookie']
    message = re[re.find('[['):re.find(']]') + 2]
    res = str(json.loads(eval("'" + message + "'")))
    print(res)
    if "选课成功" in res:
        return 200
    elif "课堂无课余量" in res:
        return 404
    elif "验证码" in res:
        api.Justice(req_id)
        return 403
    else:
        return 500

from requests_html import  HTMLSession
def has_free(kecheng_code, xuhao):
    global cookies
    check_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page=1&perpage=500'
    # sess=HTMLSession()
    # res=sess.get(check_url, cookies=cookies, headers=check_classheader)
    # print(res.text)
    res = requests.get(check_url, cookies=cookies, headers=check_classheader)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('div', id='current')
    class_trs = table.find_all('tr')[1:]
    for tr in class_trs:
        if kecheng_code in tr.text:
            has_free = tr.find('input')
            if has_free:
                class_code = has_free["value"].strip()
                class_name = tr.find('div', class_='hide').text.strip()
                class_name = re.search("】(.*)", class_name).group(1)
                if xuhao in class_name:
                    print("有课余量：")
                    print(class_name)
                    print(class_code)
                    hashkey, answer, req_id = getCode(cookies=cookies)
                    result = post_request(cookies=cookies, class_code=class_code, hashkey=hashkey, answer=answer,
                                          req_id=req_id)
                    if result == 200:
                        return True
    return False


if __name__ == '__main__':

    username = str(input("輸入學號："))
    password = str(input("輸入mis密碼："))
    kecheng_code = input("輸入課程號，逗号隔开：").split(',')
    kecheng_code = [str(i) for i in kecheng_code]
    xuhao = input("輸入序号，逗号隔开：").split(',')
    xuhao = [str(i) for i in xuhao]

    # username = '18251076'
    # password = '10962905'
    # kecheng_code = ['85L074T']
    # xuhao = ["11"]
    time_delay = 0.5
    retry_max = 1000
    reset = False
    i = 0
    retry_num = 0
    # test_post()
    cookies = get_Session()
    while True:
        try:
            if retry_num > retry_max:
                reset = True
                retry_num = 0
                cookies = get_Session()
                continue
            if i == len(kecheng_code):
                i = 0
            if has_free(kecheng_code=kecheng_code[i], xuhao=xuhao[i]):
                print(username, password)
                print("搶課完成" + str(kecheng_code[i]))
                break
                # continue
            else:
                print('retry_time : ' + str(retry_num))
                i += 1
                retry_num += 1
                reset = False
        except Exception as e:
            print(e)
            continue
