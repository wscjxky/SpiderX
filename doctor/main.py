
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

year = 2004
browser = webdriver.Chrome('/home/kaiyuan_xu/PycharmProjects/SpiderX/doctor/chromedriver')
for y in range(13):
    for m in range(1,13):
        url='http://www.phsciencedata.cn/Share/frameset?__report=ReportAgeMonth.rptdesign&years=%s&diseaseId=17&months=%s&__sessionId=20190418_012310_643'% \
            (y + year,m)
        browser.get(url)
        print(url)
        # time.sleep(1)
        element = WebDriverWait(browser, 100).until(
            EC.visibility_of_element_located((By.TAG_NAME, "th"))
        )
        res = browser.page_source
        with open('%s_%s_result.html' % (year + y,m), 'w')as f:
            f.write(res)
browser.close()

import json
import xml
import xml.dom.minidom as xmldom
import re
import requests

# data = {}
# dic = {}
# with open('header.txt', 'r')as f:
#     ls = f.readlines()
#     for l in ls:
#         arr = l.strip('\n').split(':')
#         dic[arr[0]] = arr[1].strip(' ')
# print(dic)
# with open('data.txt', 'r')as f:
#     ls = f.readlines()
#     for l in ls:
#         arr = l.strip('\n').split(':')
#         data[arr[0]] = arr[1].strip(' ')
# year = 2005
# month = 1
# for y in range(13):
#     # base_url = 'http://www.phsciencedata.cn/Share/frameset?__report=ReportZoneYear.rptdesign&years=%s&disease' \
#     #            'Id=17&__sessionId=20190418_003138_664'%(year + y)
#     base_url='http://www.phsciencedata.cn/Share/frameset?__report=ReportZoneYear.rptdesign&years=%s&di' \
#              'seaseId=17&__sessionId=20190418_004348_838'%(y+year)
#     print(base_url)
#     # for m in range(12):
#     # payload = '<soap:Envelope xmlns:soap="http://schemas.xm' \
#     #           'lsoap.org/soap/envelope/"><Body xmlns="http://schemas.xmlsoap.org/soap/' \
#     #           'envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/birt"><Operation><T' \
#     #           'arget><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><Oprand><Name>year' \
#     #           's</Name><Value>%s</Value></Oprand><Oprand><Name>__isdisplay__years</Name><Value>%s</Value></Opran' \
#     #           'd><Oprand><Name>diseaseId</Name><Value>17</Value></Oprand><Oprand><Name>__isdisplay__diseaseId</Name><Valu' \
#     #           'e>17</Value></Oprand><Oprand><Name>__page</Name><Value>1</Value></Oprand><Oprand><Name>__svg</Name><Value>false</Value></Oprand><Oprand><Name>__page</Name><Value>1</Value></Oprand><Oprand><Name>__taskid</Name><Value>2019-3-18-8-31-40-669</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>' % (
#     #                   year + y,year + y)
#     payload='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><Body xmlns="http' \
#             '://schemas.xmlsoap.org/soap/envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/bi' \
#             'rt"><Operation><Target><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><' \
#             'Oprand><Name>years</Name><Value>%s</Value></Oprand><Oprand><Name>__isdisplay__years</Name><Value>%s</' \
#             'Value></Oprand><Oprand><Name>diseaseId</Name><Value>17</Value></Oprand><Oprand><Name>__isdisplay__diseaseId<' \
#             '/Name><Value>17</Value></Oprand><Oprand><Name>__page</Name><Value>1</Value></Oprand><Oprand><Name>__svg</Name><V' \
#             'alue>false</Value></Oprand><Oprand><Name>__page</Name><Value>1</Value></Oprand><Oprand><Name>__taskid</Name><Value>' \
#             '2019-3-18-8-43-51-298</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>'%(y+year,y+year)
#     print(payload)
#     response = requests.post(base_url, data=payload, headers=dic)
#     res = (response.text)
#     res = res.replace('\n', '')
#     res = re.search("<Content>(.+)</Content>", res).group(1)
#     res = res.replace('&lt;', '<').replace('&gt;', '>').replace("&quot;", '"').replace(';&#xa0;','')
#     with open('%s_result.html' % (year + y), 'w')as f:
#         f.write(res)
#     break
#
