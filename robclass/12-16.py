import threadpool
from config import FateadmApi, robclass_headers, headers, headers_image, get_user_agent
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from YDM import *
from chaojiying import Chaojiying_Client
from chaoren import *

import sys

sys.path.append('./')
STOP_FLAG = 0
THREAD_FLAG = False
sleep_time_503 = 2
chaoren_client = Chaoren()
chaoren_client.data['username'] = 'wscjxky'  # 修改为打码账号
chaoren_client.data['password'] = 'wscjxky123'  # 修改为打码密码
chaojiying = Chaojiying_Client(
    'wscjxky', 'wscjxky123', '898146')  # 用户中心f>>软件ID 生成一个替换 96001

yundama = YDMHttp()

pd_id = "103797"
pd_key = "jz3U4Zp2DU7Rmn4ZI9MWKMVRqFR2+M0w"
app_id = "303997"  # 开发者分成用的账号，在开发者中心可以查询到
app_key = "UwlgecslQIl8kZojP+Vf7NFCQ72SC/FH"
pred_type = "40300"
api = FateadmApi(app_id, app_key, pd_id, pd_key)



def get_Session():
    BCOOKIES = {}
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Chrome(executable_path='./chromedriver.exe',
                    options=chrome_options)
    # jwc   
    if account=='jwc':
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
    # mis
    else:
        driver.get('https://mis.bjtu.edu.cn/')
        driver.maximize_window()
        elem = driver.find_element_by_css_selector('#id_loginname')
        elem.send_keys(username)
        elem = driver.find_element_by_xpath('//*[@id="id_password"]')
        elem.send_keys(password)
        elem = driver.find_element_by_xpath('//*[@id="login"]/dl/dd[2]/div/div[3]/button')
        elem.click()
        time.sleep(1)
        elem = driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[3]/div/dl/dd[1]/div/ul/li[3]/div/div[2]/h3/a')
        elem.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

    time.sleep(1)
    cookie = driver.get_cookies()
    # time.sleep(1)
    assert len(cookie) == 2

    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
    print('reload' + str(BCOOKIES))
    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
    driver.close()
    driver.quit()
    return ssrequest.cookies


# from requests_html import HTMLSession

def post_request(cookies, class_code, hashkey, img_data, pred_type="ydm"):
    global THREAD_FLAG
    # while count < 50:
    #     check_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page=1&perpage=500'
    #     res = requests.get(check_url, cookies=cookies, headers=check_classheader)
    #     count += 1
    try:

        if pred_type == "ydm":
            req_id, answer = yundama.decode(img_data, 2004, 20)
        elif pred_type == "chaoren":
            res = chaoren_client.recv_byte(img_data)
            answer, req_id = res[u'result'], res[u'imgId']
        elif pred_type == "pp":
            answer, req_id = api.Predict(40400, img_data)
        elif pred_type == "cjy":
            answer, req_id = chaojiying.PostPic(img_data, 2004)
        data = {'checkboxs': class_code,
                # 'is_cross':True,
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
            post_request(cookies, class_code, hashkey, img_data, pred_type)
        re = re.headers['Set-Cookie']
        message = re[re.find('[['):re.find(']]') + 2]
        res = str(json.loads(eval("'" + message + "'")))
        print(pred_type + "请求：" + str(data))
        print(res)
        if "选课成功" in res:
            THREAD_FLAG = True
            return 200
        elif "课堂无课余量" in res:
            return 404
        elif "验证码" in res:
            if pred_type == 'pp':
                api.Justice(req_id)
            elif pred_type == 'cjy':
                chaojiying.ReportError(req_id)
            elif pred_type == 'ydm':
                yundama.report(req_id)
            else:
                chaoren_client.report_err(req_id)
            return 403
            # 完全错误，比如有类似的课了
        else:
            return 500
    except Exception as e:
        print("139postreq bug ：" + str(e))
        return 403


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content.decode('utf8')


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def make_noise():
    try:
        import winsound
        duration = 1000  # millisecond
        freq = 500  # Hz
        winsound.Beep(freq, duration)
    except:
        import os

        duration = 1  # second
        freq = 500  # Hz
        os.system(
            'play --no-show-progress --null --channels 1 synth %s sine %f' % (
                duration, freq))


def is_free(kecheng_code, xuhao, proxy='', is_cross=False):
    global cookies, error_503
    load_url = "https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&"
    if is_cross:
        check_url = load_url + 'iframe=cross&page=1&perpage=500'
    else:
        check_url = load_url + 'iframe=school&page=1&perpage=500'
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
            print(
                "503次数:{}" + str(error_503))
            print(error_503)
            return False
            # print(503)
            # is_free(kecheng_code, xuhao, proxy=proxy, pred_type=pred_type)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 任选课的table
    table = soup.find('div', id='container')
    # 专业课的table
    # table = soup.find('div', id='current')
    # if is_cross:
        # table = soup.find('table', class_='table')
    # with open("a.html", 'w', encoding="utf-8")as f:
    #     f.write(res.text)
    try:
        if table:
            class_trs = table.find_all('tr')[1:]
            for tr in class_trs:
                for index_kecheng, k_code in enumerate(kecheng_code):
                    if k_code in tr.text:
                        has_free = tr.find('input')
                        try:
                            is_chosen = tr.find("span", class_="red").text
                            if ("选" in is_chosen):
                                print(str(index_kecheng) +
                                      str(index_kecheng) + str(k_code) + "课程已选上")
                                exit()
                        except:
                            pass
                        if has_free:
                            class_code = has_free["value"].strip()
                            class_name = tr.find('div', class_='ellipsis')
                            if class_name:
                                class_name = class_name.text.strip()
                            else:
                                class_name = tr.find(
                                    'div', class_='hide').text.strip()
                            class_name = re.search(
                                "】(.*)", class_name).group(1)
                            if xuhao[index_kecheng] in class_name:
                                print("有课余量：")
                                make_noise()
                                print(class_name)
                                print(class_code)
                                res = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/', cookies=cookies,
                                                   headers=headers_image)
                                json_data = res.json()
                                hashkey = json_data['key']
                                print(json_data)
                                img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'],
                                                        headers=headers)
                                randomNumber = random.randint(0,len(device_list)-1)
                                # result = post_request(cookies=cookies, class_code=class_code, hashkey=hashkey,
                                #                       img_data=img_data.content, pred_type=device_list[randomNumber])
                                result = start_threading(cookies=cookies, class_code=class_code, hashkey=hashkey,
                                                         img_data=img_data.content)
                                if result == 200:
                                    return True

                                else:
                                    return False
        else:
            if ("503" in res.text):
                time.sleep(sleep_time_503)
                print(503)
    except Exception as e:
        print(e)
    return False


class Success(SyntaxWarning):
    pass


def callback(request, result):
    global STOP_FLAG
    print(result)
    STOP_FLAG += 1
    if result == 200:
        raise Success
    elif result == 500:
        raise Success
device_list = ['pp', 'cjy', 'chaoren']

def start_threading(cookies, class_code, hashkey, img_data):
    global STOP_FLAG
    #  'ydm'
      # 需要处理的设备个数
    task_pool = threadpool.ThreadPool(5)  # 5是线程池中线程的个数
    request_list = []  # 存放任务列表
    # 首先构造任务列表
    for device in device_list:
        lst_vars = [cookies, class_code, hashkey, img_data, device]
        request_list.append((lst_vars, None))
    requests = threadpool.makeRequests(
        post_request, request_list, callback=callback)
    [task_pool.putRequest(req, block=True, timeout=20) for req in requests]
    try:
        # print(f"STOP_FLAG:{STOP_FLAG}")
        # if STOP_FLAG >= 4:
        #     STOP_FLAG = 0
        #     return False
        task_pool.wait()
    except Success as e:
        print(e)
        return 200


if __name__ == '__main__':
    import os 

    username =os.sys.argv[1]
    password = os.sys.argv[2]
    kecheng_code = os.sys.argv[3].split(',')
    xuhao =os.sys.argv[4].split(',')
    name = os.sys.argv[5]
    account = os.sys.argv[6]
    is_cross = False
    if "跨年级" in name:
        is_cross = True
        print("该用户是跨年级用户")
    assert len(kecheng_code) == len(xuhao)
    print(len(kecheng_code), len(xuhao))
    print(username, password, kecheng_code, xuhao, name,account)
    error_503 = 0
    retry_max = 50000
    reset = False
    i = 0
    retry_num = 0
    # is_cross = True
    cookies = get_Session()
    while True:
        if THREAD_FLAG:
            print(username, password)
            print("搶課完成")
            break
        try:
            time.sleep(0.7)

            if is_free(kecheng_code=kecheng_code, xuhao=xuhao, is_cross=is_cross):
                print(username, password)
                print("搶課完成" + str(kecheng_code[i]))
                make_noise()
                break
            else:
                if retry_num % 20 == 0:
                    print(name + " " + str(time.strftime("%H:%M:%S")
                                           ) + '  retry_time : ' + str(retry_num))
                i += 1
                retry_num += 1
                reset = False
        except Exception as e:
            # raise (e)
            print(e)
            continue
