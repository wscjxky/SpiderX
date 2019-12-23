from aip import AipOcr
import threadpool
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import sys
import time
import requests
from config import FateadmApi, robclass_headers, headers, headers_image, get_user_agent
import json
sys.path.append('./')
STOP_FLAG = 0
THREAD_FLAG = False
client = AipOcr("18075034", "GcBPfVEhCu6vXtEK1Qgu5wTL",
                "YeDKFlWFCwZ84DWallNL4d3u9BUTmq1V")
""" 读取图片 """
pd_id = "103797"
pd_key = "L5oPz3M0cbHJhiOfzs1gTk4oW9b2yVsB"
app_id = "303997"  # 开发者分成用的账号，在开发者中心可以查询到
app_key = "o8SL2OUcncoCeYCDuN7PhS/54Ns/wepQ"
pred_type = "10400"
api = FateadmApi(app_id, app_key, pd_id, pd_key)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def login():
    url = "http://newxk.urp.seu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do#cvUnProgramCourse"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('disable-infobars')
    driver = Chrome(executable_path='chromedriver',
                    options=chrome_options)
    driver.get(url)
    img_src = driver.find_element_by_xpath(
        '//*[@id="vcodeImg"]').get_attribute("src")
    print(img_src)
    image = requests.get(img_src)
    # 百度
    # res = client.basicAccurate(image.content)
    # print(res)
    # if not res:
    #     print("验证码识别出错")
    #     print(res)
    #     return False
    # verify = res['words_result'][0]['words']
    verify, req_id = api.Predict(pred_type, image.content)
    print(f"img_src:{img_src}")
    verify = verify.strip(" ").strip()
    token = img_src[len(
        "http://newxk.urp.seu.edu.cn/xsxkapp/sys/xsxkapp/student/vcode/image.do?vtoken="):]
    # 使用验证码结果请求得到token
    driver.quit()
    return verify, token


def get_token(username, passwd, code, token):
    url = f"http://newxk.urp.seu.edu.cn/xsxkapp/sys/xsxkapp/student/check/login.do?timestrap=1576940187824&loginName={username}&loginPwd={passwd}&verifyCode={code}&vtoken={token}"
    data = requests.get(url).text
    data = json.loads(data)
    if not data['msg'] == "登录成功":
        print("登陆失败")
        print(data)
        return False
    print("登陆成功")
    return data['data']["token"]


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


def main_rob(token, class_code, class_type):
    url = "http://newxk.urp.seu.edu.cn/xsxkapp/sys/xsxkapp/elective/volunteer.do"
    headers = {}
    with open("header.txt", 'r')as f:
        res = f.readlines()
        for l in res:
            l = l.replace(": ", ":").replace("\n", "")
            value = l.split(":")[1]
            if "http:" in l:
                value = "http:"+l.split(":")[2]
            key = l.split(":")[0]
            headers[key] = value
    headers["token"] = token
    res = requests.post(
        url, data=f"addParam=%7B%22data%22%3A%7B%22operationType%22%3A%221%22%2C%22studentCode%22%3A%22213192260%22%2C%22electiveBatchCode%22%3A%2291952a1cf3d1496a8570861909edba09%22%2C%22teachingClassId%22%3A%22{class_code}%22%2C%22isMajor%22%3A%221%22%2C%22campus%22%3A%221%22%2C%22teachingClassType%22%3A%22{class_type}%22%7D%7D", headers=headers)
    res = json.loads(res.text)
    return res['msg']


if __name__ == '__main__':
    class_code = "201920203B07M106001"
    username = "213192260"
    passwd = "beyond0607"
    count = 0
    # 推荐课程
    # class_type="TJKC"
    # 方案外选课
    class_type = "FAWKC"
    while True:
        code, ts = login()
        token = get_token(username, passwd, code, ts)
        print (token)
        if token:
            break
    while True:
        # try:
            res = main_rob(token, class_code, class_type)
            if "添加选课志愿成功" in res or "该课程已经存在选课结果中" in res:
                print(res)
                print(class_code,class_type)
                make_noise()
                print("抢课成功")
                break
            # elif "" in res['msg']:
            elif "请求数据与登录者身份不一致" in res:
                print(res) 
                while True:
                    code, token = login()
                    token = get_token(username, passwd, code, token)
                    if token:
                        break
            else:
                if count % 10 == 0:
                    print(res)
                count += 1
                time.sleep(5)
            
        # except Exception as e :
        #     print(e)
        #     pass

