with open("cmp.txt",'w',encoding="utf8")as f :

    for page in range(1,6):
        url=f"http://sxh.51job.com/Union/hotComany?page={page}&take=1000&shpkid=c7be2d86-ed94-4163-8a88-c1f8f9d9f0ad&type=&companyName=&isHot=false"
        import requests
        import json
        pre_url="http://sxh.51job.com/unite/company.html?&coname="
        data=requests.get(url)
        data.encoding='utf-8'
        #解析xml格式内容，将字符串转为特殊的对象
        data = json.loads(data.text)
        for cmp in data['list']:
            new_link=pre_url+cmp['cmpName']
            f.write(new_link+"\n")
