import base64
import hashlib
import json
import time

import requests

FATEA_PRED_URL = "http://pred.fateadm.com"

robclass_headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control':
                        'no-cache', 'Connection': 'keep-alive', 'Content-Type':
                        'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'dean.bjtu.edu.cn',
                    'Origin': 'https://dean.bjtu.edu.cn', 'Pragma': 'no-cache',
                    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=load&iframe=cross',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/74.0.3729.169 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
                    }

# with open('robclass_header.txt', 'r')as f:
#     ls = f.readlines()
#     for l in ls:
#         arr = l.strip('\n').split(':')
#         robclass_headers[arr[0]] = arr[1].strip(' ')
# print(robclass_headers)
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
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
        code = rsp.pred_rsp.value
        if code == '' or len(code) < 3:
            self.Justice(rsp.request_id)
        return code, rsp.request_id

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


