import http.client, mimetypes, urllib, json, time, requests

######################################################################

class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'
    username = 'wscjxky'
    password = 'wscjxky123'
    appid = '9685'
    appkey = '563046555fd1666bb307629c63d78aaa'

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response
    
    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        res = requests.post(url, files=files, data=fields)
        return res.text


#     # 初始化
# yundama = YDMHttp()
#
# # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
# a=open('test.jpg','rb')
# answer, req_id = yundama.decode(a, 2003, 10)
# print(answer, req_id)
# yundama.report(req_id)

######################################################################
#
# a=input("输入验证码:")
# pic=open('temp.png','wb')
# pic.write(img_data)
#
# print(a)
