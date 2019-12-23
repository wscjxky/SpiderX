import threadpool
from config import FateadmApi, robclass_headers, headers, headers_image, get_user_agent
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import sys
import time
sys.path.append('./')
STOP_FLAG = 0
THREAD_FLAG = False


def choose_class(class_name):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Chrome(executable_path='chromedriver',
                    options=chrome_options)
    url = 'http://njwxt.swupl.edu.cn/jwglxt/xtgl/login_slogin.html'
    driver.get(url)
    # driver.maximize_window()
    elem = driver.find_element_by_xpath('//*[@id="yhm"]')
    elem.send_keys(username)
    elem = driver.find_element_by_xpath('//*[@id="mm"]')
    elem.send_keys(password)
    elem = driver.find_element_by_xpath('//*[@id="dl"]')
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_xpath('//*[@id="index_wdyy"]/li[1]/a')
    elem.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    elem = driver.find_element_by_xpath(
        '//*[@id="searchBox"]/div/div[1]/div/div/div/div/input')
    elem.send_keys(class_name)
    search_btn_elem = driver.find_element_by_xpath(
        '//*[@id="searchBox"]/div/div[1]/div/div/div/div/span/button[1]')
    search_btn_elem.click()
    while True:
        time.sleep(1)
        full_elem=driver.find_element_by_xpath(
            '//*[@id="contentBox"]/div[2]/div[1]/div[2]/table/tbody/tr/td[18]')
        is_full = full_elem.is_displayed()
        # print(full_elem.text)
        search_btn_elem.click()
        if not is_full:
            make_noise()
            chosen_btn_elem= driver.find_element_by_xpath(
            '//*[@id="contentBox"]/div[2]/div[1]/div[2]/table/tbody/tr/td[20]/button')
            chosen_btn_elem.click()
            return True



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


if __name__ == '__main__':
    with open('zhengfa.txt', 'r', encoding='utf8')as f:
        ls = f.readlines()
        for line in ls:
            if line != '' and "#" not in line:
                line = line.strip('\n')
                data = line.split(' ')
                username = data[0]
                password = data[1]
                class_name = data[2].split(',')
                name = data[3]
    is_cross = False
    print(username, password, class_name, name)
    error_503 = 0
    retry_max = 50000
    reset = False
    i = 0
    retry_num = 0
    # is_cross = True
    result = choose_class(class_name=class_name)
    if result == True:
        print("抢课完成",username, password)
