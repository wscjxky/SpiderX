import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# 人工智能 83429  83129 82580


# code_list = ['87010']
code_list = ['87065','87050']


from  predict import *
# 200959
# 16281112
username = '18251134'
password = '85399028'
time_delay = 2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    ,
    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'
    ,
    'Host': 'dean.bjtu.edu.cn',
    'Pragma': 'no-cache',
    'Connection': 'keep-alive',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # "Connection": "close",
}
headers_image = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    ,
    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'

    ,
    'Upgrade-Insecure-Requests': '1',
    'Host': 'dean.bjtu.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Pragma': 'no-cache',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache'
    # "Connection": "close",
}


def get_Session():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
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
        '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[2]/td[1]/div/div/h5/a')
    elem.click()
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    cookie = driver.get_cookies()

    # 获取浏览器cookies
    # BCOOKIES = {
    #     'csrftoken':'J03JagXCbfyH9jHGGwL27HDadOPrgCaJsNIq68xXtDbW5cuL3LNtt22laPhfZSnn',
    #     'sessionid':'1f36fnd964r5k24urh3kyh9j4losrdw5'
    # }
    BCOOKIES = {}
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
        print(i["name"], i["value"])
    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
    return ssrequest, driver


#

def post_met(ssrequest, class_code, hashkey, answer):
    time.sleep(time_delay)
    # 验证
    # print(requests.get('https://dean.bjtu.edu.cn/notice/item/',
    #                    cookies=ssrequest.cookies,
    #                    # headers=headers
    #                    ))
    # time.sleep(random.randint(0, 1))
    # requests.adapters.DEFAULT_RETRIES = 2
    # s = requests.session()
    # s.keep_alive = False
    data = {'checkboxs': class_code,
            'hashkey': hashkey,
            'answer': answer
            }
    # data = {
    #     'checkboxs': class_code,
    #     'hashkey': '7c271f0fbc2f832f5598b98bf7c807ee29c09501',
    #     'answer': int(answer)
    # }
    re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       cookies=ssrequest.cookies,
                       headers=headers_image,
                       # data={
                       #     'select_id': 135194
                       #  }
                       # re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       #                    cookies=ssrequest.cookies,
                       #                    data={
                       #                        'select_id': 135193
                       #                     }
                       data=data)
    if len(re.text) != 41:
        # {"msg": "\u9a8c\u8bc1\u7801\u9519\u8bef"}
        pass
    # print(re.text)
    # print(class_code)
    print(re.status_code)
    print(data)
    re.close()


def getCode():
    re = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/',
                      cookies=ssr.cookies,
                      headers=headers_image,
                      )
    print(re)
    json_data = re.json()
    hashkey = json_data['key']
    print(json_data)
    img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'], headers=headers)
    if os.path.isfile('image/' + json_data['image_url'][len('/captcha/image/'):-1] + '.jpg'):
        print('发现大事情联系我')
    with open('image/' + json_data['image_url'][len('/captcha/image/'):-1] + '.jpg', 'wb')as f:
        f.write(img_data.content)
    answer = TestFunc(img_data.content)
    with open('image.json', 'a')as f:
        f.write(hashkey + ' ' + answer + '\n')
    return hashkey, answer


def main():
    ssr, driver = get_Session()
    driver.close()
    re = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/',
                      cookies=ssr.cookies,
                      headers=headers_image,
                      )
    json_data = re.json()
    hashkey = json_data['key']
    print(json_data)
    img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'])
    # '/captcha/image/1e92c5121600c54ae93ee46e7887a887cc6a015d/'
    # img_data = requests.get('https://dean.bjtu.edu.cn/captcha/image/c6a3e2848e7ebe216b12d5e4bfdeb6ddbe4ccfbf/')
    answer = TestFunc(img_data.content)
    # print(json_data)
    # print(hashkey)
    for i in code_list:
        post_met(ssr, i, hashkey, answer)


def download():
    time_start = time.time()
    time_end = time.time()
    ssr, driver = get_Session()
    driver.close()
    while True:
        cost_time = time_end - time_start
        if cost_time > 1000:
            ssr, driver = get_Session()
            driver.close()
        re = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/',
                          cookies=ssr.cookies,
                          headers=headers_image,
                          )
        json_data = re.json()
        print(json_data)
        img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'])
        print(img_data)
        with open(json_data['image_url'][-20:-1] + '.jpg', 'wb') as f:
            f.write(img_data.content)
        time_end = time.time()


if __name__ == '__main__':
    import time

    # ssr, driver = get_Session()
    # post_met(ssr, code_list[0], 'asdasd12312asdzxcasd', 2)
    global hashkey, answer, driver, ssr
    ssr, driver = get_Session()
    driver.quit()
    hashkey, answer = getCode()
    print(hashkey, answer)
    time_start = time.time()
    time_start1 = time.time()
    while True:
        try:
            time_end = time.time()
            time_end1 = time.time()
            cost_time = time_end - time_start
            cost_time1 = time_end1 - time_start1
            print(cost_time)
            if cost_time > 120:
                print('reset code ' + str(cost_time))
                hashkey, answer = getCode()
                time_start = time.time()
            if cost_time1 > 2400:
                print('reset driver ' + str(cost_time1))
                ssr, driver = get_Session()
                driver.quit()
                time_start1 = time.time()
            for i in code_list:
                post_met(ssr, i, hashkey, answer)
        except Exception as e:
            with open('error', 'a')as f:
                f.write(str(e))
            pass

# if __name__ == '__main__':
#     # ssr, driver = get_Session()
#     # post_met(ssr)
#     import time
#     global ssr
#     ssr, driver = get_Session()
#     # driver.quit()
#     post_met(ssr, code_list[0])
#     time_start = time.time()
#     # while True:
#     #     try:
#     #         # time.sleep(random.randint(0, 1))
#     #         time_end = time.time()
#     #         cost_time = time_end - time_start
#     #         # if cost_time > 1000:
#     #         for i in code_list:
#     #             post_met(ssr, i)
#     #     # 超过最大链接数
#     #     except Exception as e:
#     #         try:
#     #             driver.quit()
#     #         except:
#     #             print('a')
#     #         finally:
#     #             ssr, driver = get_Session()
#     #             driver.quit()
#     #             time_start = time.time()
#     #             cost_time = 0
