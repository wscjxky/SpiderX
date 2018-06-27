from bs4 import BeautifulSoup
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import base64
import hashlib
import json
import requests

# username = '16281117'
# password = '111516'
username = '16281011'
password = 'jj1307mmm'
cookie_name = '16281011'
FATEA_PRED_URL = "http://pred.fateadm.com"
time_delay = 1
cache_time = 1000
# 课程号在第一个就是1
# class_code = [1]

# 课程号在第一个就是1
# class_code = [1]
class_code = [314, 315, 274, 282]
retry_max = 1200
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    ,
    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/'
    ,
    'Host': 'dean.bjtu.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Pragma': 'no-cache',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache'
    # "Connection": "close",
}
check_classheader = {"Host": "dean.bjtu.edu.cn",
                     "Connection": "keep-alive",
                     "Accept": "*/*",
                     "X-Requested-With": "XMLHttpRequest",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                     "Referer": "https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/",
                     "Accept-Encoding": "gzip, deflate, br",
                     "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8"
                     }


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

        return rsp

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
    print('code : ' + rsp.pred_rsp.value)
    #
    # just_flag    = False
    # if just_flag :
    #     if rsp.ret_code == 0:
    #         #识别的结果如果与预期不符，可以调用这个接口将预期不符的订单退款
    #         # 退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
    #         api.Justice( rsp.request_id)

    # card_id         = "123"
    # card_key        = "123"
    # 充值
    # api.Charge(card_id, card_key)
    return rsp.pred_rsp.value


def get_Session():
    BCOOKIES = {}
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
    for i in cookie:  # 添加cookie到CookieJar
        BCOOKIES[i["name"]] = i["value"]
    print('reload' + str(BCOOKIES))
    ssrequest = requests.session()
    requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
    driver.close()
    return ssrequest.cookies


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
    print((re.text))

    print(re.status_code)
    # print(data)
    re.close()


def getCode(cookies):
    re = requests.get('https://dean.bjtu.edu.cn/captcha/refresh/',
                      cookies=cookies,
                      headers=headers_image,
                      )
    json_data = re.json()
    hashkey = json_data['key']
    print(json_data)
    img_data = requests.get('https://dean.bjtu.edu.cn' + json_data['image_url'], headers=headers)
    answer = TestFunc(img_data.content)
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


def post_request(cookies, class_code, hashkey, answer):
    data = {'checkboxs': class_code,
            'hashkey': hashkey,
            'answer': answer
            }
    re = requests.post('https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit',
                       cookies=cookies,
                       headers=headers_image,
                       data=data)
    # if len(re.text) != 41:
    #     return True
    print((re.text))
    print((re.content))

    print(re.status_code)
    # print(data)
    re.close()


def has_free(class_code, reset=False):
    global cookies
    print(reset)
    check_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=school&page=1&perpage=500'
    if reset:
        cookies = get_Session()
    res = requests.get(check_url, cookies=cookies, headers=check_classheader)
    soup = BeautifulSoup(res.text, 'html.parser')
    class_trs = soup.find_all("tr")
    class_tr = class_trs[class_code]
    has_free = class_tr.find('input')
    class_name = class_tr.find_all('td')[2].text
    print(class_name)
    if has_free:
        print('ok')
        class_code = has_free.attrs['value']
        hashkey, answer = getCode(cookies=cookies)
        post_request(cookies=cookies, class_code=class_code, hashkey=hashkey, answer=answer)
        return True
    else:
        return False


if __name__ == '__main__':
    reset = False
    i = 0
    retry_num = 0
    cookies = get_Session()
    while True:
        try:
            if retry_num > retry_max:
                reset = True
                continue
            if i == len(class_code):
                i = 0
            if has_free(class_code=class_code[i], reset=reset):
                # break
                continue
            else:
                print('retry_time : ' + str(retry_num))
                print('code ： ' + str(class_code[i]))
                i += 1
                retry_num += 1
                reset = False

        except Exception as e:
            print(e)
            reset = True
            continue
