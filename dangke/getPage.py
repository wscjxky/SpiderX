import re

def run_script(rid,s_rid):
    if s_rid==None:
        s_rid="None"
    print(rid,s_rid)
    query='''
    var alist=$(".plyr__time--duration").text().split(":");
    console.log(alist);
      var atv=10;
if(alist.length==2){
     atv=parseInt(alist[0])*60+parseInt(alist[1]);
}
else{
         atv=parseInt(alist[0])*3600+parseInt(alist[1])*60+parseInt(alist[2]);

}
    console.log(atv);

function GetQueryString(name)

{

    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)"); 

    var r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则

    if(r!=null)return  unescape(r[2]); return null;

}
function study_time(){


$.ajax({
    type: "POST",
    cache: false,
    async:false,

    dataType: "json",
    url: "/ybdy/lesson/study_time",
    data: {
        rid: "'''+str(s_rid)+'''",
        study_time: atv*1000,
        _xsrf: $(":input[name='_xsrf']").val()
    },
    success: function (res) {
        console.log(res)
    }
});

}

function gettime(){
                        console.log(  atv*1000)
    $.ajax({
                
        type: "POST",
        cache: false,
        async:false,
        dataType: "json",
        url: "/ybdy/lesson/current_time",
        data: {
            rid: GetQueryString("r_id"),
            time:atv,
            _xsrf: $(":input[name='_xsrf']").val()
        },
        success: function (res) {
                    console.log(res)

        }
    });

}

function getLess(){
    return $(".video_goback").attr("href").replace(/[^0-9]/ig,"");
 }
function p(){
    $.ajax({
        type: "POST",
    cache: false,
    dataType: "json",
    url: "http://wsdx.nwafu.edu.cn/ybdy/lesson/resource_record",
data: 
    { rid: "'''+str(rid)+'''",
    resource_id:  GetQueryString("r_id"),
    video_id:  GetQueryString("v_id"),
    lesson_id: getLess(),
    _xsrf: $(":input[name='_xsrf']").val()}
,
success: function (data) {
    console.log(data);
        flag = false;
    window.clearInterval(loop_flag);
    if (Number(data.code) == 1) {
        public_alert(1, ["我知道了"], '<i class="iconfont">&#xe633;</i><p>当前视频播放完毕！</p><p></p>', 'public_cont1', function () {
            window.location.reload()
        });
    $(".public_cont").css("left", "40%");
    $('.plyr__controls').show();
}
}
    });
}

for (var i=0;i<3;i++){
    setTimeout(gettime,1000*i);

    for (var j = 0 ; j < 4 ; j++)
    {
        setTimeout(study_time,1000*(j+i));
    }


}
    setTimeout(gettime,10000);
setTimeout(p,11000);


'''    
    return query
dic={}
with open('header.txt', 'r')as f:
    ls = f.readlines()
    for l in ls:
        arr = l.strip('\n').split(':')
        dic[arr[0]] = arr[1].strip(' ')
print(dic)
import time
href_list=[]
from bs4 import BeautifulSoup 
with open("test.html",'r',encoding="utf8")as f:
    soup=BeautifulSoup(f.read())
    divs=(soup.find_all("div",class_="study_plan2"))[:-6]
    for d in divs:
        href=(d.find('a').get('href'))
        href_list.append(href)
        id=href[len("/ybdy/lesson/play?v_id="):-len("&r=video&t=2")]
        # print(id)
print(href_list)
href_list=['/ybdy/lesson/play?v_id=2155&r=video&t=2', '/ybdy/lesson/play?v_id=2091&r=video&t=2', '/ybdy/lesson/play?v_id=2173&r=video&t=2', '/ybdy/lesson/play?v_id=2137&r=video&t=2', '/ybdy/lesson/play?v_id=2162&r=video&t=2', '/ybdy/lesson/play?v_id=2097&r=video&t=2', '/ybdy/lesson/play?v_id=2057&r=video&t=2']
import requests
href_list=href_list[4:]
url="https://authserver.nwafu.edu.cn/authserver/login?service=http://wsdx.nwafu.edu.cn/user/cas_login/login"
from selenium import webdriver
driver=webdriver.Chrome()
username="2019055825"
paaswd="Nwafu19980105"
driver.get(url)
elem = driver.find_element_by_xpath('//*[@id="username"]')
elem.send_keys(username)
elem = driver.find_element_by_xpath('//*[@id="password"]')
elem.send_keys(paaswd)


elem = driver.find_element_by_xpath(
        '//*[@id="send-btn"]')
elem.click()
driver.get("http://wsdx.nwafu.edu.cn/user/lesson")
for url in href_list:
    driver.get("http://wsdx.nwafu.edu.cn"+url)
    soup=BeautifulSoup(driver.page_source)
    lesson_video_list=soup.find('ul',class_="lesson_video_list")
    l_video_list=lesson_video_list.find_all("li")
    for less in l_video_list:
        a_less=less.find('a').get('href')
        new_url="http://wsdx.nwafu.edu.cn"+a_less
        driver.get(new_url)
        # v_id=re.findall('v_id=(.*?)&',a_less)[0]
        # r_id=re.findall('r_id=(.*?)&',a_less)[0]
        if(less==l_video_list[0]):
            html=driver.page_source
            p_data=re.findall('_record",data:{(.*?)_xsrf',html.replace('\n','').replace('\t','').replace(" ",""))[0]
            rid=re.findall('rid:"(.*?)"',p_data)[0]
            print(p_data)
            p_data=re.findall('study_time",data:{(.*?)_xsrf',html.replace('\n','').replace('\t','').replace(" ",""))[0]
            print(p_data)
            s_rid=re.findall('rid:"(.*?)"',p_data)[0]
        # lesson_id=re.findall('lesson_id:"(.*?)"',p_data)[0]

        # xsrf=soup.find('input',attrs={'name':'_xsrf'})

        # timesp=soup.find('span',class_="plyr__time--duration")
        # alist=timesp.split(":");
        # atv=int(alist[0])*60+int(alist[1]);
        # print(xsrf,v_id,r_id,rid,lesson_id,atv)
        time.sleep(3)
        query=run_script(rid,s_rid)
        res=driver.execute_script(query)
        time.sleep(20)
        print(new_url)

    #     break
    # break
