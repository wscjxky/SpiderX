
 
# 最下面有入口方法调用例子
# 最下面有入口方法调用例子
# 最下面有入口方法调用例子
 
import requests,datetime,hmac,hashlib,base64,urllib,json,decimal
from urllib import parse
from config_module.get_config import get_config_file
from log_module import log_print
from wechat_module.send_to_wechat import send_to_wechat
 
# 获取配置文件对象
#cf = get_config_file()
 
# 获取request请求相关参数
request_timeout = 5
request_retry_count = 5
 
# 获取交易对信息
huobi_symbol = 'ethusdt'
# 获取下单类型信息
huobi_buy_deal_type = 'buy-market'
huobi_sell_deal_type = 'sell-market'
# 获取交易量
huobi_deal_amount = '1'
 
# 获取access_key,等验证信息
huobi_access_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
huobi_secret_key = 'YYYYYYYYYYYYYYYYYYYYYYYY'
huobi_sub_account_id = 'xxxxxxx'
huobi_api_domain = 'huobi_api_domain'
huobi_api_SignatureMethod = 'HmacSHA256'
huobi_api_SignatureVersion = '2'
 
 
# 设置请求Headers
headers={
    'Content-Type': 'application/json',
}
 
# 对请求参数进行签名，返回含签名的完整请求URL 例子：https://api.huobi.pro/v1/order/orders/place?AccessKeyId=XXXXXXX-XXXXXXXX-XXXXXXX-XXXXXXXX&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2019-08-17T06%3A33%3A25&Signature=gMVL3yC/IUOYdo2KWJoAoHb%2BSVaX85cKyaI4%2BlbtgX4%3D
def api_signature(method,param,url_path):
    # 创建时间戳
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    #print('timestam: %s' % (timestamp))
 
    # 对时间戳进行URL编码
    timestamp_url_encode = parse.quote(timestamp)
 
    # 定义每个接口都必须的默认的请求参数
    default_param = {
        'AccessKeyId' : huobi_access_key,
        'SignatureMethod' : huobi_api_SignatureMethod,
        'SignatureVersion' : huobi_api_SignatureVersion,
        'Timestamp' : timestamp_url_encode,
    }
 
    # GET请求需要对所有请求参数进行签名，POST则不用
    if method == 'GET':
        default_param.update(param)
 
    # 对字典的排序，按key已ascii码排序
    sorted_param = dict(sorted(default_param.items(), key=lambda d: d[0], reverse=False))
    #print(sorted_param)
 
    # 拼接URL请求参数
    # 定义拼接在URL后面的请求参数
    url_param = ''
    # 循环param字典拼接请求参数
    #print(len(sorted_param))
    # 初始化循环次数，如果循环次数等于字典长度就不在后面加连接符 &
    a = 0
    for param_key,param_value in sorted_param.items():
        # 每次循环 循环次数自增1
        a+=1
        # url参数拼接
        url_param = url_param + '%s=%s' % (param_key,param_value)
        # 如果循环次数少于字典长度则在后面加连接符&
        if a < len(sorted_param):
            url_param = url_param + '&'
    #print(url_param)
 
 
    # 拼接需要进行签名计算的字符串
    need_secret_string = '%s\n%s\n%s\n%s' % (method,huobi_api_domain,url_path,url_param)
    #print('need_secret_string: %s' % need_secret_string)
 
    # 生成签名加密字符串
    # 调整字符串编码
    need_secret_string_encode = need_secret_string.encode(encoding='UTF8')
    huobi_secret_key_encode = huobi_secret_key.encode(encoding='UTF8')
    # 进行加密计算 并 签名
    secret_string = hmac.new(huobi_secret_key_encode,need_secret_string_encode,digestmod=hashlib.sha256).digest()
    # 签名
    signature = base64.b64encode(secret_string)
    signature = signature.decode()
    signature = parse.quote(signature)
    #print(signature)
 
    # 把签名字符串拼接到请求url
    url_param = url_param + '&Signature=%s' % (signature)
    #print(url_param)
 
    # 拼接出最终完整url
    url = 'https://%s%s?%s' % (huobi_api_domain,url_path,url_param)
    #print(url)
    return url
 
 
# 获取火币最新行情 返回json格式（字典格式）
def get_api_ticker():
    # 循环10次，尝试次数为10次
    flag = True
    a = 0
    while(flag):
        # 每次循环+1 到10次时退出死循环
        a+=1
        if a == request_retry_count: flag = False
        try:
            url = 'https://api.huobi.pro/market/detail/merged?symbol=%s' % (huobi_symbol)
            r = requests.get(url,timeout=request_timeout)
            log_print.info('get ticker success %s ' % r.text)
            # 判断是否发送成功，如不成功则抛出异常
            request_dict = r.json()
            request_status = request_dict['status']
            if request_status != 'ok': raise Exception('get huobi api error')
            # 消息成功发送，停止死循环
            flag = False
            return request_dict
        except Exception as e:
            log_print.exception(e)
            #send_to_wechat(e)
 
 
# 以GET或POST请求API（签名验证的形式）返回结果的字典格式
def request_api(method,url_path,param):
 
    # 把请求参数进行签名，获得含有签名的完整请求URL
    url = api_signature(method,param,url_path)
 
    # 请求循环10次，尝试次数为10次
    flag = True
    a = 0
    while(flag):
        # 每次循环+1 到10次时退出死循环
        a+=1
        if a == request_retry_count: flag = False
        try:
            if method == 'GET':
                r = requests.get(url,timeout=request_timeout)
            if method == 'POST':
                r = requests.post(url, data=json.dumps(param), headers=headers, timeout=request_timeout)
            log_print.info('request api success, result: %s ' % r.text)
            # 判断是否发送成功，如不成功则抛出异常
            request_dict = r.json()
            request_status = request_dict['status']
            if request_status != 'ok': raise Exception('request huobi api error')
            # 消息成功发送，停止死循环
            flag = False
            return request_dict
        except Exception as e:
            log_print.exception(e)
            #send_to_wechat(e)
 
 
# 获取账号信息
def get_api_user_info():
    log_print.info('request_api: get_api_user_info(获取账号信息)')
 
    # 请求请求方式
    method = 'GET'
 
    # 接口url_path
    url_path = '/v1/account/accounts'
 
    # 定义接口请求参数
    param = {}
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
 
# 获取账号余额
def get_api_user_balance():
    log_print.info('request_api: get_api_user_balance(获取账余额)')
 
    # 请求请求方式
    method = 'GET'
 
    # 接口请求URL
    url_path = '/v1/account/accounts/%s/balance' % (huobi_sub_account_id)
    # 定义请求参数
    param = {
        'account-id': huobi_sub_account_id,
    }
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
 
# 获取订单详情
def get_api_order_info(order_id):
    log_print.info('request_api: get_api_order_info(获取订单详情)')
 
    # 请求请求方式
    method = 'GET'
 
    # 接口请求URL
    url_path = '/v1/order/orders/%s' % (order_id)
    # 定义请求参数
    param = {
        'order-id': order_id,
    }
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
 
# 获取订单成交明细(有成交价)
def get_api_order_deal_detail(order_id):
    log_print.info('request_api: get_api_order_deal_detail(获取订单成交明细)')
 
    # 请求请求方式
    method = 'GET'
 
    # 接口请求URL
    url_path = '/v1/order/orders/%s/matchresults' % (order_id)
    # 定义请求参数
    param = {
        'order-id': order_id,
    }
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
# 下单请求
def post_api_order_place(deal_type,deal_amount):
    log_print.info('request_api: post_api_order_place(下单)')
 
    # 请求请求方式
    method = 'POST'
 
    # 接口请求URL
    url_path = '/v1/order/orders/place'
 
    param = {
        'account-id' : huobi_sub_account_id,
        'symbol' : huobi_symbol,
        'type' : deal_type,
        'amount' : deal_amount,
        #'price' : 100.00,
        'source' : 'api',
    }
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
# 撤销订单
def post_api_order_cancel(order_id):
    log_print.info('request_api: post_api_order_cancel(撤销订单)')
 
    # 请求请求方式
    method = 'POST'
 
    # 接口请求URL
    url_path = '/v1/order/orders/%s/submitcancel' % (order_id)
 
    param = {
        'order-id' : order_id,
    }
 
    # 请求接口
    result_dict = request_api(method,url_path,param)
    #print(result_dict)
 
    # 返回结果
    return result_dict
 
# 获取账户某币种的数量 返回字符串类型
def get_api_user_coin_balance(coin_type):
    # 初始化币种数量变量
    coin_balance = None
 
    # 获取用户所有币种的数量
    user_balance = get_api_user_balance()
    user_coin_balance_list = user_balance['data']['list']
    # 循环所有币种 找到要的币种 并获得数量
    for user_coin_balance in user_coin_balance_list:
        if user_coin_balance['currency'] == coin_type and user_coin_balance['type'] == 'trade':
            coin_balance = user_coin_balance['balance']
 
    return coin_balance
 
 
# 方法调用例子
#get_api_ticker()
#get_api_user_info()
#get_api_user_balance()
#get_api_order_info(45118400565)
#get_api_order_deal_detail(44988853101)
#post_api_order_place(huobi_sell_deal_type,'0.0050')
#post_api_order_cancel(44801145100)
