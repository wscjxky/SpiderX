import requests
from  requests_html import HTMLSession

from robclass.config import robclass_headers


# data={
# # next: /o/authorize/?response_type=code&client_id=qamiHUSTlVvP6J9iMoPO7yvlb7zEU7qYRVK9P0xf&state=1559453905&redirect_uri=https://mis.bjtu.edu.cn/auth/callback/?redirect_to=/home/
# # csrfmiddlewaretoken: y8R28SRWKyGkexumyj10oIwDfkIkGJJVmnYOL79pfElI0XDyDh7kFPEN83ggF19k
# 'loginname': '15281106',
# 'password': 'wscjxky123'
# }
# url='https://cas.bjtu.edu.cn/auth/login/?next=/o/authorize/%3Fresponse_type%3Dcode%26client_id%3DqamiHUSTlVvP6J9iMoPO7yvlb7zEU7qYRVK9P0xf%26state%3D1559453905%26redirect_uri%3Dhttps%3A//mis.bjtu.edu.cn/auth/callback/%3Fredirect_to%3D/home/'
# res=session.post(url,headers=robclass_headers,data=data)
# # res.html.render()
# print(res.html.text)
def req(img,im):
    session=HTMLSession()
    ss = session.get('https://www.baidu.com/')
    print(ss.text)
    print(img)

import threadpool
poolsize = 100
pool = threadpool.ThreadPool(poolsize)
parm=[1,2]
parm1=[2,3]
rs = threadpool.makeRequests(req, [(parm,None),(parm1,None)])
[pool.putRequest(req) for req in rs]
pool.wait()
