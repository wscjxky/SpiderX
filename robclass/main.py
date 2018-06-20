from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver import Firefox

# import pymongo
import logging
import requests
from  .fateadm_api import TestFunc
# from config import *


# user_id_str = '16231199'
# password_str = '297659'
user_id_str = '15281106'
password_str = 'wscjxky123'
xpath_str = ''
delta = 0.2
try_max_count = 1000


def search(driver):
    wait = WebDriverWait(driver, 10)

    try:
        driver.get('https://mis.bjtu.edu.cn/home/')
        name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#id_loginname'))
        )
        password = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#id_password'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#form1 > div > div > button'))
        )
        name.send_keys(user_id_str)
        password.send_keys(password_str)
        submit.click()
    except TimeoutException:
        return search(driver)
    driver.maximize_window()
    ShaungXueWei = driver.find_element_by_css_selector(
        '#wrap > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > div > div > table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div > a')

    ShaungXueWei.click()
    elem = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[2]/td[1]/div/div/h5/a')
    elem.click()

    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    time.sleep(3)

    try:
        elem = driver.find_element_by_css_selector('#sidebar > div > div.nav-wrap > ul > li:nth-child(4) > a > span')
        elem.click()
    except:
        elem = driver.find_element_by_xpath('//*[@id="menu-toggler"]')
        print(elem.id)
        elem.click()
        print('End')

    driver.find_element_by_xpath('//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[1]/ul/li[2]/a').click()


def duoXuan(driver, i):
    # current > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > label:nth-child(1)
    driver.find_element_by_css_selector('#current > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(' + str(
        i) + ') > td:nth-child(1) > label').click()
    return True


def XuanKe(driver):
    driver.find_element_by_xpath('//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a').click()
    i_list = [9,10]
    flag = False
    try_cnt = 1
    i = 0
    while not flag:
        try:
            # 2代表第一个框框
            duoXuan(driver, i_list[i])
            # / html / body / div[4] / div / div / div[3] / button[1]
            driver.find_element_by_css_selector(
                'body > div.bootbox.modal.in > div > div > div.modal-footer > button.btn.btn-sm.btn-info').click()
            driver.find_element_by_xpath('//*[@id="select-submit-btn"]').click()
            print("OK!")
            print("You have try " + str(try_cnt) + " times.")
        except Exception as e:
            print(i)
            print(e)
            if i == len(i_list) - 1:
                i = 0
            else:
                i += 1
            driver.refresh()
            try_cnt += 1
            if try_cnt > try_max_count:
                driver.quit()
                main()
            time.sleep(delta)


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-infobars')
    driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
    search(driver)
    XuanKe(driver)


if __name__ == '__main__':
    main()
