from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time
import pymongo
import logging
import time
import os, sys
import base64
import hashlib
import time
import urllib
import json
import string
import requests

FATEA_PRED_URL = "http://pred.fateadm.com"


def LOG(log):
    # 不需要测试时，注释掉日志就可以了
    # print(log)
    log = None


class TmpObj():
    def __init__(self):
        self.value = None


class Rsp():
    def __init__(self):
        self.ret_code = -1
        self.cust_val = 0.0
        self.err_msg = "succ"
        self.pred_rsp = TmpObj()

    def ParseJsonRsp(self, rsp_data):
        if rsp_data is None:
            self.err_msg = "http request failed, get rsp Nil data"
            return
        jrsp = json.loads(rsp_data)
        self.ret_code = int(jrsp["RetCode"])
        self.err_msg = jrsp["ErrMsg"]
        self.request_id = jrsp["RequestId"]
        if self.ret_code == 0:
            rslt_data = jrsp["RspData"]
            if rslt_data is not None and rslt_data != "":
                jrsp_ext = json.loads(rslt_data)
                if "cust_val" in jrsp_ext:
                    data = jrsp_ext["cust_val"]
                    self.cust_val = float(data)
                if "result" in jrsp_ext:
                    data = jrsp_ext["result"]
                    self.pred_rsp.value = data


def CalcSign(usr_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((usr_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


def CalcCardSign(cardid, cardkey, timestamp, passwd):
    md5 = hashlib.md5()
    md5.update(passwd + timestamp + cardid + cardkey)
    return md5.hexdigest()


def HttpRequest(url, body_data):
    rsp = Rsp()
    post_data = body_data
    header = {
        'User-Agent': 'Mozilla/5.0',
    }
    rsp_data = requests.post(url, post_data, headers=header)
    rsp.ParseJsonRsp(rsp_data.text)
    return rsp


class FateadmApi():
    def __init__(self, app_id, app_key, usr_id, usr_key):
        self.app_id = app_id
        if app_id is None:
            self.app_id = ""
        self.app_key = app_key
        self.usr_id = usr_id
        self.usr_key = usr_key
        self.host = FATEA_PRED_URL

    def SetHost(self, url):
        self.host = url
        #

    # 查询余额
    #
    def QueryBalc(self):
        tm = str(int(time.time()))
        sign = CalcSign(self.usr_id, self.usr_key, tm)
        param = {
            "user_id": self.usr_id,
            "timestamp": tm,
            "sign": sign
        }
        url = self.host + "/api/custval"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("query succ ret: {} cust_val: {} rsp: {} pred: {}".format(rsp.ret_code, rsp.cust_val, rsp.err_msg,
                                                                          rsp.pred_rsp.value))
        else:
            LOG("query failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

        #

    # 查询网络延迟
    #
    def QueryTTS(self, pred_type):
        tm = str(int(time.time()))
        sign = CalcSign(self.usr_id, self.usr_key, tm)
        param = {
            "user_id": self.usr_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": pred_type,
        }
        if self.app_id != "":
            #
            asign = CalcSign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/qcrtt"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("query rtt succ ret: {} request_id: {} err: {}".format(rsp.ret_code, rsp.request_id, rsp.err_msg))
        else:
            LOG("predict failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

        #

    # 识别验证码
    #
    def Predict(self, pred_type, img_data, head_info=""):
        tm = str(int(time.time()))
        sign = CalcSign(self.usr_id, self.usr_key, tm)
        img_base64 = base64.b64encode(img_data)
        param = {
            "user_id": self.usr_id,
            "timestamp": tm,
            "sign": sign,
            "predict_type": pred_type,
            "img_data": img_base64,
        }
        if head_info is not None or head_info != "":
            param["head_info"] = head_info
        if self.app_id != "":
            #
            asign = CalcSign(self.app_id, self.app_key, tm)
            param["appid"] = self.app_id
            param["asign"] = asign
        url = self.host + "/api/capreg"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("predict succ ret: {} request_id: {} pred: {} err: {}".format(rsp.ret_code, rsp.request_id,
                                                                              rsp.pred_rsp.value, rsp.err_msg))
        else:
            LOG("predict failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg.encode('utf-8')))
            if rsp.ret_code == 4003:
                # lack of money
                LOG("cust_val <= 0 lack of money, please charge immediately")
        return rsp

        #

    # 从文件进行验证码识别
    #
    def PredictFromFile(self, pred_type, file_name, head_info=""):
        with open(file_name, "rb") as f:
            data = f.read()
        return self.Predict(pred_type, data, head_info)

        #

    # 识别失败，进行退款请求
    # 注意:
    #    Predict识别接口，仅在ret_code == 0时才会进行扣款，才需要进行退款请求，否则无需进行退款操作
    # 注意2:
    #   退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
    #
    def Justice(self, request_id):
        if request_id == "":
            #
            return
        tm = str(int(time.time()))
        sign = CalcSign(self.usr_id, self.usr_key, tm)
        param = {
            "user_id": self.usr_id,
            "timestamp": tm,
            "sign": sign,
            "request_id": request_id
        }
        url = self.host + "/api/capjust"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("justice succ ret: {} request_id: {} pred: {} err: {}".format(rsp.ret_code, rsp.request_id,
                                                                              rsp.pred_rsp.value, rsp.err_msg))
        else:
            LOG("justice failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp

        #

    # 充值接口
    #
    def Charge(self, cardid, cardkey):
        tm = str(int(time.time()))
        sign = CalcSign(self.usr_id, self.usr_key, tm)
        csign = CalcCardSign(cardid, cardkey, tm, self.usr_key)
        param = {
            "user_id": self.usr_id,
            "timestamp": tm,
            "sign": sign,
            'cardid': cardid,
            'csign': csign
        }
        url = self.host + "/api/charge"
        rsp = HttpRequest(url, param)
        if rsp.ret_code == 0:
            LOG("charge succ ret: {} request_id: {} pred: {} err: {}".format(rsp.ret_code, rsp.request_id,
                                                                             rsp.pred_rsp.value, rsp.err_msg))
        else:
            LOG("charge failed ret: {} err: {}".format(rsp.ret_code, rsp.err_msg.encode('utf-8')))
        return rsp


def TestFunc(imgdata):
    pd_id = "103797"  # 用户信息页可以查询到pd信息
    pd_key = "B9G8DxjiEK7U8Gr+dVS93rJyL2P5gtoH"
    app_id = "303997"  # 开发者分成用的账号，在开发者中心可以查询到
    app_key = "o8SL2OUcncoCeYCDuN7PhS/54Ns/wepQ"
    # 识别类型，
    # 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
    pred_type = "50100"
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    bal = api.QueryBalc()

    # #如果不是通过文件识别，则调用Predict接口
    # file_name       = imgurl+".jpg"
    # rsp             = api.PredictFromFile( pred_type, file_name)
    rsp = api.Predict(pred_type, imgdata)
    return rsp.pred_rsp.value


chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-infobars')
driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
# client = pymongo.MongoClient('localhost',27017)
# mis = client['mis']
# schedule = mis['schedule']
wait = WebDriverWait(driver, 10)
url = 'https://mis.bjtu.edu.cn/home/'
URL = 'http://jwc.bjtu.edu.cn'
username = '16321143'
password = 'dabai2VK'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    ,
    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'
    ,
    'Host': 'dean.bjtu.edu.cn',
    'Pragma': 'no-cache',
    'Connection': 'keep-alive',
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    # "Connection": "close",
}
def login(url, username, password):
    driver.get(url)
    # time.sleep(1)
    driver.maximize_window()
    elem = driver.find_element_by_css_selector('#id_loginname')
    elem.send_keys(username)
    elem = driver.find_element_by_xpath('//*[@id="id_password"]')
    elem.send_keys(password)
    elem = driver.find_element_by_xpath('//*[@id="form1"]/div/div/button')
    # time.sleep(2)
    elem.click()


def solve():
    elem = driver.find_element_by_xpath(
        '//*[@id="wrap"]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[2]/td[1]/div/div/h5/a')
    elem.click()
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    driver.maximize_window()
    try:
        elem = driver.find_element_by_css_selector('#sidebar > div > div.nav-wrap > ul > li:nth-child(4) > a > span')
        elem.click()
    except:
        elem = driver.find_element_by_xpath('//*[@id="menu-toggler"]')
        elem.click()
    # class_code = [6, 4, 7, 3]
    class_code = [6]
    driver.find_element_by_xpath('//*[@id="sidebar2"]/div[1]/div[1]/div/ul/li[2]/ul/li[1]/a').click()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="current"]/iframe'))
    # classn = '//*[@id="current"]/table/tbody/tr[18]/td[1]/label'
    input_css = '/html/body/form/input[1]'
    elem = WebDriverWait(driver, 1, 0.1).until(EC.presence_of_element_located((By.XPATH, input_css)))
    # elem.send_keys('安全')
    elem.send_keys('网球')
    submit_btn = driver.find_element_by_xpath('/html/body/form/button')
    submit_btn.click()
    # while True:
    #     submit_btn = WebDriverWait(driver, 1.2, 0.1).until(
    #         EC.presence_of_element_located((By.XPATH, '/html/body/form/button')))
    #     submit_btn.click()
    i = 0
    while True:
        if i >= len(class_code) - 1:
            i = 0
        try:
            confirm_btn = WebDriverWait(driver, 1.2, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "select-submit-btn"]')))
            classn = '//*[@id="container"]/table/tbody/tr[' + str(class_code[i]) + ']/td[1]/input'
            elem = driver.find_element_by_xpath(classn)
            elem.click()
            confirm_btn.click()
            driver.switch_to.default_content()
            elem = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/div/img').get_attribute('src')
            img_data = requests.get(elem,headers=headers)
            ans = TestFunc(img_data.content)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/div/input[2]').send_keys(ans)
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
            print("end")
        except Exception as e:
            print(e)
            submit_btn = WebDriverWait(driver, 1.2, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/form/button')))
            submit_btn.click()
            i += 1


def main():
    login(url, username, password)
    solve()


if __name__ == '__main__':
    main()
    # '//*[@id="selected-container"]/table/tbody/tr[2]/td[3]'
