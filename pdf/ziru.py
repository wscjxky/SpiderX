
import time
import winsound
while 1:
    try:
        url="http://tj.ziroom.com/x/796827728.html"
        from requests_html import HTMLSession
        #启动
        session = HTMLSession()
        r = session.get(url)
        Z_name = r.html.find('.Z_name')
        status=Z_name[0].find('i')[0].attrs['class'][1]
        print(status)
        if "release" in status:
            print("ok")
            winsound.Beep(600,5000)
        time.sleep(3600/2)
    except Exception as e :
        print(e)
        winsound.Beep(600,5000)
        break
        