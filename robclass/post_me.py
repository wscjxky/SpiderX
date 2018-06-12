import random

import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import time

# 【80L145Q】VHDL及设计实践 81886
# 【80L204Q】虚拟化与云计算 82578
# 人工智能 83429  83129 82580
# 机械学习 82182 82781
# code_list = ['81886', '82578', '83429', '83129', '82580', '82182', '82781']
code_list = ['82578']


def get_Session():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
    wait = WebDriverWait(driver, 10)
    url = 'https://mis.bjtu.edu.cn/home/'
    username = '15281106'
    password = 'wscjxky123'

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
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    cookie = driver.get_cookies()
    # 获取浏览器cookies
    BCOOKIES = {
    }
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
        print(i["name"], i["value"])

    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)

    return (ssrequest), driver


headers = {
    "Connection": "close",
}


def post_met(ssrequest, class_code):
    # 验证
    # print(requests.get('https://dean.bjtu.edu.cn/notice/item/',
    #                    cookies=ssrequest.cookies,
    #                    # headers=headers
    #                    ))
    # time.sleep(random.randint(0, 1))
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       cookies=ssrequest.cookies,
                       data={'checkboxs': class_code},
                       headers=headers
                       )
    re.close()
    print(class_code)
    print(re)


def main():
    ssr, driver = get_Session()
    for i in code_list:
        post_met(ssr, i)


if __name__ == '__main__':
    # ssr, driver = get_Session()
    # post_met(ssr)
    import time
    global ssr
    ssr, driver = get_Session()
    driver.quit()
    time_start = time.time()
    while True:
        try:
            # time.sleep(random.randint(0, 1))
            time_end = time.time()
            cost_time = time_end - time_start
            # if cost_time > 1000:
            for i in code_list:
                post_met(ssr, i)
        # 超过最大链接数
        except Exception as e:
            try:
                driver.quit()
            except:
                print('a')
            finally:
                ssr, driver = get_Session()
                driver.quit()
                time_start = time.time()
                cost_time = 0
