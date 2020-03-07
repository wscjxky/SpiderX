# from huobi import RequestClient
# from huobi.model import *

# from huobi.base.printobject import PrintMix

# request_client = RequestClient()
# trades = request_client.get_market_trade(symbol="ethusdt")
# if len(trades):
#     for trade in trades:
#         trade.print_object()
#         print()
import time
import requests
import json


buy_limit_price = 1910
buy_trade_limit = 2000

sell_trade_limit = 1870
sell_limit_price = 1100


def get_buy():
    a = requests.get("https://otc-api-sz.eiijo.cn/v1/data/trade-market?coinId=3&currency=1&tradeType=buy&currPage=1&payMethod=0&country=37&blockType=general&online=1&range=0&amount="+str(buy_trade_limit))
    data = (json.loads(a.content))
    return data["data"][:5]


def get_sell():
    url = "https://otc-api.eiijo.cn/v1/data/trade-market?coinId=3&currency=1&tradeType=sell&currPage=1&payMethod=0&country=37&blockType=general&online=1&range=0&amount="+str(sell_trade_limit)
    a = requests.get(url)
    data = (json.loads(a.content))
    return data["data"][:5]


def order():
    url = "https://otc-api.eiijo.cn/v1/order/orders/place"
    req_data = {
        "account-id": "100009",
        "amount": "10.1",
        "source": "api",
        "symbol": "bchusdt",
        "type": "buy-limit"
    }
    res=requests.post(url,req_data)
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


count = 0
while True:
    data_buy = get_buy()
    data_sell=get_sell()
    if count%20==0:
        print("有人买:"+str(data_buy[0]['price']))
        print("有人卖:"+str(data_sell[0]['price']))

    for i in (data_buy):
        if(float(i['price']) >= buy_limit_price and float(i['minTradeLimit'] <= buy_trade_limit)):
            print(i)
            make_noise()
            exit()
    for i in (data_sell):
        if(float(i['price']) <= sell_trade_limit and float(i['minTradeLimit'] <= sell_trade_limit)):
            print(i)
            make_noise()
            exit()
    count += 1
    time.sleep(1)


