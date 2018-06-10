import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
import time

# DB = redis.Redis(host='47.94.251.202', port=6379,db=10,password='wscjxky123')

s = requests.session()
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-infobars')
driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
wait = WebDriverWait(driver, 10)
url = 'https://mis.bjtu.edu.cn/home/'
URL = 'http://jwc.bjtu.edu.cn'
xuanke_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'
username = '16231199'
password = '297659'
headers_or = {
           'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/67.0.3396.79 Safari/537.36',

           }
headers = {'Host': 'dean.bjtu.edu.cn',
           'Connection': 'keep-alive',
           'Content-Length': '15',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache',
           'Origin': 'https://dean.bjtu.edu.cn',
           'Upgrade-Insecure-Requests': '1',
           'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/67.0.3396.79 Safari/537.36',
           'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Accept-Encoding': 'gzip,deflate,br',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def login(url, username, password):
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
    BCOOKIES = {
    }
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
        print(i["name"], i["value"])

    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)

    print(ssrequest.cookies)
    print(requests.get('https://dean.bjtu.edu.cn/notice/item/',
                        cookies=ssrequest.cookies,
                    # headers=headers
                 ))
    print(requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                        cookies=ssrequest.cookies,
                        data={'checkboxs': '83083'},
                        ))
    # 进教务
    # function
    # post_to(url, args, csrf_token)
    # {
    #     var
    # form = $("<form></form>");
    # var
    # default_csrf = window.csrf_token | | '';
    # form.attr({"action": url, "method": "post"}).append($(csrf_token | | default_csrf));
    #
    # $.each(args, function(key, value)
    # {
    #     var
    # input = $("<input type='hidden'>");
    # input.attr({"name": key}).val(value).appendTo(form);
    # });
    #
    # form.appendTo(document.body).submit();
    # document.body.removeChild(form[0]);
    # }

    # elem = driver.find_element_by_xpath(
    #     '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[2]/td[1]/div/div/h5/a')
    # elem.click()
    # handles = driver.window_handles
    # driver.switch_to.window(handles[-1])
    # print(driver.page_source)
    # # 点击选课
    # wait.until(expected.visibility_of_element_located((By.XPATH, '//*[@id="sidebar"]/div/div[1]/ul/li[4]/a')))
    # elem = driver.find_element_by_xpath('//*[@id="sidebar"]/div/div[1]/ul/li[4]/a')
    # print(driver.page_source)
    # elem.click()
    # # 点击网上选课
    # wait.until(
    #     expected.visibility_of_element_located((By.XPATH, '//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a')))
    # elem = driver.find_element_by_xpath('//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a')
    # print(elem)
    # elem.click()


def xuanKe():
    # 点击选课
    wait.until(expected.visibility_of_element_located((By.XPATH, '//*[@id="sidebar"]/div/div[1]/ul/li[4]/a')))
    elem = driver.find_element_by_xpath('//*[@id="sidebar"]/div/div[1]/ul/li[4]/a')
    print(driver.page_source)
    elem.click()
    # 点击网上选课
    wait.until(
        expected.visibility_of_element_located((By.XPATH, '//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a')))
    elem = driver.find_element_by_xpath('//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a')
    print(elem)
    elem.click()


def main():
    login(url, username, password)
    # solve()
    # xuanKe()

    # try:
    #     login(url, username, password)
    #     solve()
    #     xuanKe()
    #     time.sleep(2)
    #     while True:
    #         time.sleep(0.5)
    #         driver.refresh()
    #         # if driver
    #         #     //*[@id="select-submit-btn"]
    #         time.sleep(0.5)
    #
    #     driver.close()
    # except Exception as e:
    #     print(e)
    #     driver.close()
    #     main()


if __name__ == '__main__':
    main()
    # '//*[@id="selected-container"]/table/tbody/tr[2]/td[3]'
