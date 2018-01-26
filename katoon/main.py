# -*- coding: utf-8 -*- #

import os
import urllib2
from bs4 import BeautifulSoup
import json
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import time
Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}



if __name__ == '__main__':

    url='http://manhua.dmzj.com/baoshizhiguo/26765.shtml#@page=2'
    # url = 'http://www.kuman.com/rank-renqi/'
    # req = urllib2.Request(url, headers=Headers)
    # try:
    #     data = urllib2.urlopen(req).read()
    #     print data
    #
    # except:
    #     print 404
    # soup = BeautifulSoup(data, 'html.parser')
    # tag = soup.find_all('div', class_="p-img")

    driver = webdriver.PhantomJS(executable_path="phantomjs\phantomjs.exe")
    driver.implicitly_wait(3)  # 隐性等待，最长等30秒
    driver.get(url)

    img=driver.find_element_by_css_selector("div[id='center_box']>img")#css选择器可以在chrome里调试格式 $("主标签>次标签[属性='']")
    # WebDriverWait(driver, 2,0.5).until(img.is_displayed())
    print img
    # driver.quit()
