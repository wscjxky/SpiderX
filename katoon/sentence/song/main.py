# -*- coding: utf-8 -*- #
from nosql import DB
import os
import socket
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from constant import *

def requestByFixfox(url):
    time.sleep(TIME_SLEEP)
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', firefox_options=options)
    wait = WebDriverWait(driver, timeout=5)
    driver.get(url)
    wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'songNameA')))
    data= driver.page_source
    driver.quit()
    return data

def requestUrl(url):
    print url
    time.sleep(TIME_SLEEP)
    req=urllib2.Request(url,headers=Headers)
    data = urllib2.urlopen(req).read()
    return data
def getSinger():
    for i in range(2,3):
        url=SOURCE_URL+'/geshou/'+str(i)+'.htm'
        try:
            data = '''<html xmlns="http://www.w3.org/1999/xhtml"><head><script type="text/javascript" async="" src="http://cpro.baidustatic.com/cpro/ui/pr.js"></script><script charset="utf-8" src="https://atanx.alicdn.com/t/tanxssp/probe.js" async="" mod_name="tanxssp-probe"></script><script src="http://ope.tanx.com/ex?i=mm_114132704_13204673_70572034&amp;cb=jsonp_callback_42719&amp;callback=&amp;userid=&amp;o=&amp;f=&amp;n=&amp;r=&amp;cg=a493a8ac53da59b91dbc28c149025b7d&amp;pvid=ccfc898d69e0f03a115cbb1a37d091d0&amp;u=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;psl=0&amp;fp=1.HavSOf7PtFAmIp~_VExvOX2CtT8zJR-BqQrVJi1gZkRWqqV_lWLSvU.UTF-8.vxph1zQy1oT2aOSagWig-qQAOaAbTSdC6cod0TDP6YBTkg.Q.ka4hbi" async=""></script><script charset="utf-8" async="" src="http://atanx.alicdn.com/t/tanxssp.js?_v=12"></script><script type="text/javascript" charset="gbk" id="tanx-s-mm_114132704_13204673_70572034" async="" src="http://p.tanx.com/ex?i=mm_114132704_13204673_70572034"></script>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="x-ua-compatible" content="IE=edge">
<title>阿杜歌曲大全_阿杜最新歌曲_九酷音乐</title>
<meta name="keywords" content="阿杜,阿杜歌曲,阿杜歌曲大全,阿杜全部歌曲,阿杜好听的歌,阿杜最新歌曲">
<meta name="description" content="阿杜">
<link rel="alternate" media="only screen and(max-width:640px)" href="http://m.9ku.com/geshou/2.htm">
<meta http-equiv="mobile-agent" content="format=xhtml; url=http://m.9ku.com/geshou/2.htm">
<meta http-equiv="mobile-agent" content="format=html5; url=http://m.9ku.com/geshou/2.htm">
<link href="/css/base.css" rel="stylesheet" type="text/css">
<link href="/css/singerNew.css?v=2" rel="stylesheet" type="text/css">
<script type="text/javascript" async="" src="http://1.hnssyhbkj.com/smqugb.js"></script><script src="http://push.zhanzhang.baidu.com/push.js"></script><script src="//hm.baidu.com/hm.js?a5de315acb973b8e6da83458c9e456d3"></script><script src="http://dsp.zz123.com/watch.js?69aFb86X39f3WW4755V1"></script><script type="text/javascript" src="/js/script/jquery.js"></script>
</head>
<body><iframe style="width: 0px; height: 0px; display: none;" src="http://cdn.tanx.com/t/acookie/acbeacon2.html#mm_114132704_13204673_70572034"></iframe>
<script type="text/javascript" src="/js/script/topcommon.js"></script><script src="http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js" type="text/javascript"></script><script>(function() {  var kp = document.createElement("script");  kp.src = "http://dsp.zz123.com/watch.js?69aFb86X39f3WW4755V1";  var a = document.getElementsByTagName("script")[0];   a.parentNode.insertBefore(kp, a);})();</script>
<script type="text/javascript" src="/js/script/asyncbox.v1.4.5.js"></script>
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?a5de315acb973b8e6da83458c9e456d3";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
<script>
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    }
    else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
</script>
<div class="top-bar">
<div class="box clearfix">
<div class="fl topBarLink"><a class="topBarLink01" style="cursor:pointer;" onclick="this.style.behavior='url(#default#homepage)';this.setHomePage('http://www.9ku.com/?sy');return(false);">设为首页</a>&nbsp;&nbsp;<a class="topBarLink02" onclick="if(document.all){window.external.addFavorite('http://www.9ku.com/?sc','九酷音乐网 - 国内最好的MP3下载音乐网站 (www.9ku.com)')}else if(window.sidebar){window.sidebar.addPanel('九酷音乐网 - 国内最好的MP3下载音乐网站 (www.9ku.com)','http://www.9ku.com/?sc','')}" style="cursor:pointer;">加入收藏</a>&nbsp;&nbsp;<a href="http://www.9ku.com/gbook/" target="_blank" style="color:blue;">意见箱</a> | <a href="http://www.9ku.com/diange/" target="_blank">点歌台</a> | <a href="http://www.9ku.com/love/" target="_blank">许愿墙</a> | <a href="/wannianli.htm" target="_blank">万年历</a> | <a href="http://www.9ku.com/zj/z2017.htm">专辑归档</a> | <a href="/" style="color:#FF0000;"><b><u>进入九酷音乐首页</u></b></a></div>
<div class="fr" id="jiukulogin"><div class="topLogin"><div class="webLogin">[ <a href="http://yun.9ku.com/user/login" target="_login" class="color">九酷帐号登录</a> ]或[ <a href="http://yun.9ku.com/user/register" target="_register" class="color">注册</a> ]</div><div class="appLogin" style="width:132px;"></div></div></div>
<script type="text/javascript" src="/js/script/denglu.js"></script>
</div>
</div>
<div class="headerWrap">
<div class="box header clearfix">
<div class="logo"><a href="/" title="九酷音乐"><img alt="九酷音乐" src="/images/base/logo.png"></a></div>
<div class="logoSide clearfix">
<div class="history">
<div class="historyBox">
<div class="historyHd"><p>我听过的歌</p></div>
<div class="historyBd">
<p class="hisQing clearfix"><a href="javascript:hisplayall();" id="playHis">全部播放</a> <a href="javascript:delcok();" id="qingkong">清空记录</a></p>
<ul class="hisList clearfix" id="hislist"></ul>
<div class="hisCao clearfix">
<div class="ctrBtn clearfix"><label class="allXuan" id="allXuan"><input name="allXuan" class="check" value="" onclick="javascript:hisquanxuan('hislist');" type="checkbox"> 全选</label>
<a href="javascript:hisclk('playadd','hislist');" class="allAdd">加入列表</a>
</div>
<div class="his-page"></div>
</div>
</div>
</div>
</div> <div class="search clearfix">
<div class="search-wrap clearfix">
<div class="search-bar">
<script language="javascript" src="/js/script/search.js"></script>
<div name="formsearchbox">
<div class="clearfix" style="position: relative; z-index: 1005; zoom: 1;">
<input class="search-txt input-value" x-webkit-speech="" autocomplete="off" id="ww" onkeydown="if (event.keyCode == 13) s();" type="text">
<button class="search-btn" type="button" id="btnSearch" onclick="s()"> 搜索</button>
</div>
</div>
<div id="sugResultbox" tabindex="0"></div>
<form>
</form>
</div>
<div class="srarchHot"> <strong>热门：</strong> <a target="_1" href="/play.htm" style="color:#FF2C56; font-weight:800;">随便听几首</a> <a target="_blank" href="/guangchangwu/"><font color="#0000FF">广场舞</font></a> <a target="_blank" href="/yingwen/"><font color="#0000FF">好听的英文歌</font></a> <a target="_blank" href="/wangluo/"><font color="#005bd8">网络歌曲</font></a> <a target="_blank" href="/erge/"><font color="#0000FF">儿歌</font></a> <a target="_blank" href="/laoge/"><font color="#FF0000">经典老歌500首</font></a> <a target="_blank" href="/lingsheng/"><font color="#0000FF">铃声</font></a> </div>
</div>
</div>
</div>
</div>
</div>
<div class="navWrap">
<div class="nav clearfix">
<ul class="navList clearfix">
<li id="navIndex"><a href="/" title="首页 九酷音乐网">首 页</a></li>
<li><a href="/music/" title="音乐排行榜 歌曲排行榜">歌曲排行榜</a></li>
<li><a class="active" href="/music/T_Singer.htm">歌手大全</a></li>
<li><a href="/zhuanji/taste.htm" title="音乐分类大全">音乐曲风</a></li>
<li><a href="/haoge/" title="天天好歌">天天好歌</a></li>
<li><a href="/taoge/" title="最新淘歌 网友自家专辑">淘歌</a></li>
<li><a href="/fm/" target="_blank" title="音乐电台">电台</a></li>
<li><a href="/dj/" target="_blank" title="DJ DJ舞曲">DJ舞曲</a></li>
<li><a href="/fuyin/" target="_blank" title="赞美诗">赞美诗</a></li>
<li><a href="/guangchangwu/" target="_blank" title="广场舞">广场舞</a></li>
<li><a href="/love/" target="_blank" title="许愿">许愿</a></li>
</ul>
</div>
</div>
<div class="box musicBus mt bgWrite">
<ul class="clearfix directNew">
<li><a class="directName" style="color:#3ba1e8; font-weight:800;" href="/music/t_new.htm">最新歌曲</a><a class="directPlay" title="最新歌曲" href="/music/t_new.htm" target="_blank"></a></li>
<li><a class="directName" style="font-weight:800;color:#f60;" target="_blank" href="/wangluo/">网络歌曲</a><a class="directPlay" title="快速播放-网络歌曲" href="/play.htm#zhuanti-55" target="_1"></a></li>
<li><a class="directName" style="color:#f00;" target="_blank" href="/laoge/">经典老歌</a><a class="directPlay" title="快速播放-经典老歌" href="/play.htm#zhuanti-3" target="_1"></a></li>
<li><a class="directName" target="_blank" href="/yingwen/">英文歌曲</a><a class="directPlay" title="快速播放-英文歌曲" href="/play.htm#zhuanti-66" target="_1"></a></li>
<li><a class="directName" target="_blank" href="/haoge/haoting.htm">好听的歌</a><a class="directPlay" title="2015好听的歌" href="/haoge/haoting.htm" target="_blank"></a></li>
<li><a class="directName" target="_blank" href="/feizhuliu/">非主流歌曲</a><a class="directPlay" title="好听的非主流歌曲" href="/play.htm#zhuanti-225" target="_1"></a></li>
<li><a class="directName" style="color:#e84817" target="_blank" href="/erge/">儿童歌曲</a><a class="directPlay" title="快速播放-儿童歌曲" href="/play.htm#zhuanti-15" target="_1"></a></li>
<li><a class="directName" style="color:#090;" target="_blank" href="/fuyin/">赞美诗</a><a class="directPlay" title="快速播放-基督教歌曲" href="/play.htm#zhuanti-193" target="_1"></a></li>
<li><a class="directName" style="color:#090;" target="_blank" href="/qingyinyue/">轻音乐</a><a class="directPlay" title="快速播放-轻音乐" href="/play.htm#zhuanti-263" target="_1"></a></li>
<li><a class="directName" target="_blank" href="/zhuanji/taste.htm">更多类型&gt;&gt;</a></li>
</ul>
</div>
<div class="box top"><script type="text/javascript" src="http://js.9ku.com/aaa/9kumusic/lanmu_top_1.js"></script><div id="_ucm7pmews4p"><ins class="pcowwhcdtowyga" style="width:0px;height:0px;padding-top:0px;"></ins><iframe scrolling="no" src="//pos.baidu.com/s?hei=90&amp;wid=960&amp;di=u431824&amp;ltu=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;cmi=0&amp;pss=1349x2953&amp;par=1366x768&amp;psr=1366x768&amp;dai=1&amp;pis=-1x-1&amp;ari=2&amp;ps=215x194&amp;chi=1&amp;exps=111000&amp;cec=UTF-8&amp;tlm=1515746679&amp;drs=3&amp;pcs=1349x667&amp;cja=false&amp;cfv=0&amp;cpl=0&amp;ti=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90&amp;cdo=-1&amp;dri=0&amp;dis=0&amp;tpr=1515746679456&amp;col=zh-CN&amp;dc=2&amp;ccd=24&amp;tcn=1515746679&amp;cce=true&amp;ant=0&amp;dtm=HTML_POST" width="960" height="90" frameborder="0"></iframe></div><script type="text/javascript" src="http://1.hnssyhbkj.com/qudrvyb5c.js"></script>
<script type="text/javascript" src="http://js.9ku.com/aaa/9kumusic/lanmu_top_2.js"></script><div id="_vdf9uf7q2fb" style="width: 100%;"><iframe scrolling="no" src="http://pos.baidu.com/s?hei=30&amp;wid=960&amp;di=u2568303&amp;ltu=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;dis=0&amp;ant=0&amp;par=1366x768&amp;tcn=1515746679&amp;ps=305x194&amp;ccd=24&amp;pis=-1x-1&amp;pss=1349x3043&amp;cdo=-1&amp;dtm=HTML_POST&amp;cec=UTF-8&amp;dc=2&amp;tpr=1515746679456&amp;cmi=0&amp;chi=1&amp;psr=1366x768&amp;pcs=1349x667&amp;tlm=1515746679&amp;cce=true&amp;ari=2&amp;col=zh-CN&amp;cpl=0&amp;exps=111000&amp;dai=2&amp;cja=false&amp;dri=0&amp;drs=3&amp;cfv=0&amp;ti=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90" width="960" height="30" frameborder="0"></iframe></div><script type="text/javascript" src="http://1.hnssyhbkj.com/x4djllmb79.js"></script>
<script type="text/javascript" src="http://js.9ku.com/aaa/9kumusic/lanmu_top_3.js"></script>
<script type="text/javascript" src="http://js.9ku.com/aaa/9kumusic/lanmu_top_4.js"></script></div>
<div class="box mb10">
<div class="singerWrap clearfix">
<div class="singerTop clearfix">
<div class="t-i"><img onerror="$(this).attr('src','/images/no-avatarPic95.png');" title="阿杜" src="http://aliyunimg.9ku.com/9kuimg/geshou/20160420/b2d57d85bbc88071.jpg"></div>
<div class="singerInfo">
<div class="t-t clearfix">
<h1>阿杜</h1>
<span class="rankIcon">TOP66 名</span><span class="redu">热度：<em>49,535</em></span></div>
<div class="i-t">
<p><strong>地区：</strong>东南亚　　<strong><strong>生日：</strong></strong>1973-03-11 (双鱼)
</p>
<p class="singerJiajie"><strong>简介：</strong>
阿杜，原名杜成义，生于1973年3月11日，新加坡歌手，祖籍为福建闽南，以其沙哑的嗓音闻名于华语音乐界，有很多中国歌迷。他被新加坡星探 Billy Koh 发掘，从而投身音乐事业，和 Ocean Bu <a href="javascript:{};" class="showJianjie">更多&gt;</a> </p>
</div>
<div class="clearfix singerBtn">
<a href="javascript:Addplay('600/26147/597/596/411346/26152/48561/26153/26156/598/467550/48566/356290/26149/48560/467067/60366/467549/467200/467054/208720/77587/467479/599/60363/595/208722/208552/356317/')" title="播放阿杜的热门歌曲" class="playSinger" target="_1"></a>
<a href="http://yun.9ku.com/" target="_blank" title="收藏阿杜" class="loveSinger"></a></div>
</div>
<script type="text/javascript">
		 $(function(){
		 $(".showJianjie").click(function(){
		 $(".jianjieAll").show();
		 $(".closeInfo").show();
		 return false;
		 });
		 $(".closeInfo").click(function(){
		 $(".closeInfo").hide();
		 $(".jianjieAll").hide();
		 return false;
		 })
		 })
	  </script>
<div class="closeInfo clearfix"><a href="javascript:{};">关闭</a></div>
<div class="jianjieAll">
<p>阿杜，原名杜成义，生于1973年3月11日，新加坡歌手，祖籍为福建闽南，以其沙哑的嗓音闻名于华语音乐界，有很多中国歌迷。他被新加坡星探 Billy Koh 发掘，从而投身音乐事业，和 Ocean Butterflies Music(海蝶音乐)签约。阿杜在 2002年推出第一张唱片《天黑》后，其声名即响遍东亚。</p>
</div>
</div>
<div class="singerNav">
<ul class="clearfix">
<li class="singerNav6"><a href="/geshou/2/"><em></em><span>歌手概况</span><b></b><span></span></a></li><li class="singerNav5"><a href="/geshou/2/info.htm"><em></em><span>歌手资料</span><b></b><span></span></a></li><li class="singerNav1"><a class="active" href="/geshou/2.htm"><em></em><span>歌曲</span><b>(110)</b><span>首</span></a></li>
<li class="singerNav3"><a href="/geshou/2/pic.htm"><em></em><span>图集</span><b>(1)</b></a></li><li class="singerNav4"><a href="/zj/2.htm"><em></em><span>专辑</span><b>(24)</b></a></li></ul>
</div>
<form name="form" action="/PP/" method="get">
<div class="singerMain">
<h2 class="lineTitle" style="color:#690;"><span>阿杜最新歌曲</span></h2>
<div class="singerMusic clearfix">
<ol id="f1">
<li><input value="868829@" name="Url" class="check" type="checkbox"><span class="songNum">01.</span><div class="songName"><a target="_1" href="/play/868829.htm" class="songNameA"><font>为爱投降《国民大生活》电视剧片尾曲</font></a>
</div><a href="http://www.9ku.com/geci/868829.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('868829')">加入列表</a></li><li><input value="861355@" name="Url" class="check" type="checkbox"><span class="songNum">02.</span><div class="songName"><a target="_1" href="/play/861355.htm" class="songNameA"><font>烂好人</font></a>
</div><a href="http://www.9ku.com/geci/861355.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('861355')">加入列表</a></li><li><input value="861054@" name="Url" class="check" type="checkbox"><span class="songNum">03.</span><div class="songName"><a target="_1" href="/play/861054.htm" class="songNameA"><font>一诺千年</font></a>
</div><a href="http://www.9ku.com/geci/861054.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('861054')">加入列表</a></li><li><input value="511879@" name="Url" class="check" type="checkbox"><span class="songNum">04.</span><div class="songName"><a target="_1" href="/play/511879.htm" class="songNameA"><font>话说从头</font></a>
</div><a href="http://www.9ku.com/geci/511879.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('511879')">加入列表</a></li><li><input value="467552@" name="Url" class="check" type="checkbox"><span class="songNum">05.</span><div class="songName"><a target="_1" href="/play/467552.htm" class="songNameA"><font>不提</font></a>
</div><a href="http://www.9ku.com/geci/467552.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467552')">加入列表</a></li><li><input value="467551@" name="Url" class="check" type="checkbox"><span class="songNum">06.</span><div class="songName"><a target="_1" href="/play/467551.htm" class="songNameA"><font>纯淨 天然 无害</font></a>
</div><a href="http://www.9ku.com/geci/467551.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467551')">加入列表</a></li><li><input value="467550@" name="Url" class="check" type="checkbox"><span class="songNum">07.</span><div class="songName"><a target="_1" href="/play/467550.htm" class="songNameA"><font>再唱一首</font></a>
</div><a href="http://www.9ku.com/geci/467550.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467550')">加入列表</a></li><li><input value="467549@" name="Url" class="check" type="checkbox"><span class="songNum">08.</span><div class="songName"><a target="_1" href="/play/467549.htm" class="songNameA"><font>几年了</font></a>
</div><a href="http://www.9ku.com/geci/467549.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467549')">加入列表</a></li><li><input value="467548@" name="Url" class="check" type="checkbox"><span class="songNum">09.</span><div class="songName"><a target="_1" href="/play/467548.htm" class="songNameA"><font>宠爱</font></a>
</div><a href="http://www.9ku.com/geci/467548.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467548')">加入列表</a></li><li><input value="467547@" name="Url" class="check" type="checkbox"><span class="songNum">10.</span><div class="songName"><a target="_1" href="/play/467547.htm" class="songNameA"><font>左心房</font></a>
</div><a href="http://www.9ku.com/geci/467547.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467547')">加入列表</a></li><li><input value="467479@" name="Url" class="check" type="checkbox"><span class="songNum">11.</span><div class="songName"><a target="_1" href="/play/467479.htm" class="songNameA"><font>挂失</font></a>
</div><a href="http://www.9ku.com/geci/467479.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467479')">加入列表</a></li><li><input value="467200@" name="Url" class="check" type="checkbox"><span class="songNum">12.</span><div class="songName"><a target="_1" href="/play/467200.htm" class="songNameA"><font>Valentine s Day</font></a>
</div><a href="http://www.9ku.com/geci/467200.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467200')">加入列表</a></li><li><input value="467067@" name="Url" class="check" type="checkbox"><span class="songNum">13.</span><div class="songName"><a target="_1" href="/play/467067.htm" class="songNameA"><font>离开我的自由</font></a>
</div><a href="http://www.9ku.com/geci/467067.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467067')">加入列表</a></li><li><input value="467054@" name="Url" class="check" type="checkbox"><span class="songNum">14.</span><div class="songName"><a target="_1" href="/play/467054.htm" class="songNameA"><font>第九次初恋</font></a>
</div><a href="http://www.9ku.com/geci/467054.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467054')">加入列表</a></li><li><input value="446306@" name="Url" class="check" type="checkbox"><span class="songNum">15.</span><div class="songName"><a target="_1" href="/play/446306.htm" class="songNameA"><font>阿杜 他一定很爱狙</font></a>
</div><a href="http://www.9ku.com/geci/446306.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('446306')">加入列表</a></li></ol>
<div class="setPlay"><a style="cursor:pointer;" onclick="javascript:quanxuan('f1');" class="setPlayXuan">全选/反选</a><a style="cursor:pointer;" onclick="javascript:new_lbplay();" class="setPlayPlay">播放</a><a style="cursor:pointer;" class="setPlayAdd">加入列表</a></div>
</div>
<h2 class="lineTitle"><span>阿杜最好听的歌</span></h2>
<div id="body">
<div class="singerMusic clearfix">
<ol id="fg"><li><input value="600@" name="Url" class="check" type="checkbox"><span class="songNum">01.</span><div class="songName"><a target="_1" href="/play/600.htm" class="songNameA"><font>离别</font></a>
</div><a href="http://www.9ku.com/geci/600.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('600')">加入列表</a></li><li><input value="26147@" name="Url" class="check" type="checkbox"><span class="songNum">02.</span><div class="songName"><a target="_1" href="/play/26147.htm" class="songNameA"><font>坚持到底</font></a>
</div><a href="http://www.9ku.com/geci/26147.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26147')">加入列表</a></li><li><input value="597@" name="Url" class="check" type="checkbox"><span class="songNum">03.</span><div class="songName"><a target="_1" href="/play/597.htm" class="songNameA"><font>撕夜</font></a>
</div><a href="http://www.9ku.com/geci/597.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('597')">加入列表</a></li><li><input value="596@" name="Url" class="check" type="checkbox"><span class="songNum">04.</span><div class="songName"><a target="_1" href="/play/596.htm" class="songNameA"><font>ANDY</font></a>
</div><a href="http://www.9ku.com/geci/596.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('596')">加入列表</a></li><li><input value="411346@" name="Url" class="check" type="checkbox"><span class="songNum">05.</span><div class="songName"><a target="_1" href="/play/411346.htm" class="songNameA"><font>相爱的泪水</font></a>
</div><a href="http://www.9ku.com/geci/411346.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('411346')">加入列表</a></li><li><input value="26152@" name="Url" class="check" type="checkbox"><span class="songNum">06.</span><div class="songName"><a target="_1" href="/play/26152.htm" class="songNameA"><font>你就像个小孩</font></a>
</div><a href="http://www.9ku.com/geci/26152.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26152')">加入列表</a></li><li><input value="48561@" name="Url" class="check" type="checkbox"><span class="songNum">07.</span><div class="songName"><a target="_1" href="/play/48561.htm" class="songNameA"><font>下雨的时候会想你</font></a>
</div><a href="http://www.9ku.com/geci/48561.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48561')">加入列表</a></li><li><input value="26153@" name="Url" class="check" type="checkbox"><span class="songNum">08.</span><div class="songName"><a target="_1" href="/play/26153.htm" class="songNameA"><font>下次如果离开你</font></a>
</div><a href="http://www.9ku.com/geci/26153.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26153')">加入列表</a></li><li><input value="26156@" name="Url" class="check" type="checkbox"><span class="songNum">09.</span><div class="songName"><a target="_1" href="/play/26156.htm" class="songNameA"><font>雨衣</font></a>
</div><a href="http://www.9ku.com/geci/26156.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26156')">加入列表</a></li><li><input value="598@" name="Url" class="check" type="checkbox"><span class="songNum">10.</span><div class="songName"><a target="_1" href="/play/598.htm" class="songNameA"><font>无法阻挡擋</font></a>
</div><a href="http://www.9ku.com/geci/598.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('598')">加入列表</a></li><li><input value="467550@" name="Url" class="check" type="checkbox"><span class="songNum">11.</span><div class="songName"><a target="_1" href="/play/467550.htm" class="songNameA"><font>再唱一首</font></a>
</div><a href="http://www.9ku.com/geci/467550.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467550')">加入列表</a></li><li><input value="48566@" name="Url" class="check" type="checkbox"><span class="songNum">12.</span><div class="songName"><a target="_1" href="/play/48566.htm" class="songNameA"><font>死心彻底</font></a>
</div><a href="http://www.9ku.com/geci/48566.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48566')">加入列表</a></li><li><input value="356290@" name="Url" class="check" type="checkbox"><span class="songNum">13.</span><div class="songName"><a target="_1" href="/play/356290.htm" class="songNameA"><font>梦中的情话</font></a>
</div><a href="http://www.9ku.com/geci/356290.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356290')">加入列表</a></li><li><input value="26149@" name="Url" class="check" type="checkbox"><span class="songNum">14.</span><div class="songName"><a target="_1" href="/play/26149.htm" class="songNameA"><font>放手</font></a>
</div><a href="http://www.9ku.com/geci/26149.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26149')">加入列表</a></li><li><input value="48560@" name="Url" class="check" type="checkbox"><span class="songNum">15.</span><div class="songName"><a target="_1" href="/play/48560.htm" class="songNameA"><font>哈啰</font></a>
</div><a href="http://www.9ku.com/geci/48560.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48560')">加入列表</a></li><li><input value="467067@" name="Url" class="check" type="checkbox"><span class="songNum">16.</span><div class="songName"><a target="_1" href="/play/467067.htm" class="songNameA"><font>离开我的自由</font></a>
</div><a href="http://www.9ku.com/geci/467067.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467067')">加入列表</a></li><li><input value="60366@" name="Url" class="check" type="checkbox"><span class="songNum">17.</span><div class="songName"><a target="_1" href="/play/60366.htm" class="songNameA"><font>天黑(弦乐版)</font></a>
</div><a href="http://www.9ku.com/geci/60366.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('60366')">加入列表</a></li><li><input value="467549@" name="Url" class="check" type="checkbox"><span class="songNum">18.</span><div class="songName"><a target="_1" href="/play/467549.htm" class="songNameA"><font>几年了</font></a>
</div><a href="http://www.9ku.com/geci/467549.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467549')">加入列表</a></li><li><input value="467200@" name="Url" class="check" type="checkbox"><span class="songNum">19.</span><div class="songName"><a target="_1" href="/play/467200.htm" class="songNameA"><font>Valentine s Day</font></a>
</div><a href="http://www.9ku.com/geci/467200.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467200')">加入列表</a></li><li><input value="467054@" name="Url" class="check" type="checkbox"><span class="songNum">20.</span><div class="songName"><a target="_1" href="/play/467054.htm" class="songNameA"><font>第九次初恋</font></a>
</div><a href="http://www.9ku.com/geci/467054.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467054')">加入列表</a></li><li><input value="208720@" name="Url" class="check" type="checkbox"><span class="songNum">21.</span><div class="songName"><a target="_1" href="/play/208720.htm" class="songNameA"><font>没什么好怕</font></a>
</div><a href="http://www.9ku.com/geci/208720.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208720')">加入列表</a></li><li><input value="77587@" name="Url" class="check" type="checkbox"><span class="songNum">22.</span><div class="songName"><a target="_1" href="/play/77587.htm" class="songNameA"><font>一生一世情不渝</font></a>
</div><a href="http://www.9ku.com/geci/77587.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77587')">加入列表</a></li><li><input value="467479@" name="Url" class="check" type="checkbox"><span class="songNum">23.</span><div class="songName"><a target="_1" href="/play/467479.htm" class="songNameA"><font>挂失</font></a>
</div><a href="http://www.9ku.com/geci/467479.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467479')">加入列表</a></li><li><input value="599@" name="Url" class="check" type="checkbox"><span class="songNum">24.</span><div class="songName"><a target="_1" href="/play/599.htm" class="songNameA"><font>你很好</font></a>
</div><a href="http://www.9ku.com/geci/599.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('599')">加入列表</a></li><li><input value="60363@" name="Url" class="check" type="checkbox"><span class="songNum">25.</span><div class="songName"><a target="_1" href="/play/60363.htm" class="songNameA"><font>爱字怎么写</font></a>
</div><a href="http://www.9ku.com/geci/60363.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('60363')">加入列表</a></li><li><input value="595@" name="Url" class="check" type="checkbox"><span class="songNum">26.</span><div class="songName"><a target="_1" href="/play/595.htm" class="songNameA"><font>一个人住</font></a>
</div><a href="http://www.9ku.com/geci/595.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('595')">加入列表</a></li><li><input value="208722@" name="Url" class="check" type="checkbox"><span class="songNum">27.</span><div class="songName"><a target="_1" href="/play/208722.htm" class="songNameA"><font>人狼</font></a>
</div><a href="http://www.9ku.com/geci/208722.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208722')">加入列表</a></li><li><input value="208552@" name="Url" class="check" type="checkbox"><span class="songNum">28.</span><div class="songName"><a target="_1" href="/play/208552.htm" class="songNameA"><font>听见牛在哭</font></a>
</div><a href="http://www.9ku.com/geci/208552.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208552')">加入列表</a></li><li><input value="356317@" name="Url" class="check" type="checkbox"><span class="songNum">29.</span><div class="songName"><a target="_1" href="/play/356317.htm" class="songNameA"><font>天黑 (弦乐版)</font></a>
</div><a href="http://www.9ku.com/geci/356317.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356317')">加入列表</a></li></ol><div class="setPlay"><a style="cursor:pointer;" onclick="javascript:quanxuan('fg');" class="setPlayXuan">全选/反选</a><a style="cursor:pointer;" onclick="javascript:new_lbplay();" class="setPlayPlay">播放</a><a style="cursor:pointer;" class="setPlayAdd">加入列表</a><a style="cursor:pointer;" onclick="javascript:plscgq('f1');" class="setShou">收藏所选</a></div></div>
</div>
<h2 class="lineTitle"><span>阿杜的歌</span></h2>
<div id="body"> <div class="singerMusic clearfix"><ol id="f2"><li><input value="592@" name="Url" class="check" type="checkbox"><span class="songNum">01.</span><div class="songName"><a target="_1" href="/play/592.htm" class="songNameA"><font>他一定很爱你</font></a>
</div><a href="http://www.9ku.com/geci/592.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('592')">加入列表</a></li><li><input value="594@" name="Url" class="check" type="checkbox"><span class="songNum">02.</span><div class="songName"><a target="_1" href="/play/594.htm" class="songNameA"><font>天天看到你</font></a>
</div><a href="http://www.9ku.com/geci/594.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('594')">加入列表</a></li><li><input value="593@" name="Url" class="check" type="checkbox"><span class="songNum">03.</span><div class="songName"><a target="_1" href="/play/593.htm" class="songNameA"><font>天黑</font></a>
</div><a href="http://www.9ku.com/geci/593.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('593')">加入列表</a></li><li><input value="73139@" name="Url" class="check" type="checkbox"><span class="songNum">04.</span><div class="songName"><a target="_1" href="/play/73139.htm" class="songNameA"><font>下雪</font></a>
</div><a href="http://www.9ku.com/geci/73139.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73139')">加入列表</a></li><li><input value="26150@" name="Url" class="check" type="checkbox"><span class="songNum">05.</span><div class="songName"><a target="_1" href="/play/26150.htm" class="songNameA"><font>天蝎蝴蝶</font></a>
</div><a href="http://www.9ku.com/geci/26150.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26150')">加入列表</a></li><li><input value="208721@" name="Url" class="check" type="checkbox"><span class="songNum">06.</span><div class="songName"><a target="_1" href="/play/208721.htm" class="songNameA"><font>我在你的爱情之外</font></a>
</div><a href="http://www.9ku.com/geci/208721.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208721')">加入列表</a></li><li><input value="89789@" name="Url" class="check" type="checkbox"><span class="songNum">07.</span><div class="songName"><a target="_1" href="/play/89789.htm" class="songNameA"><font>差一点</font></a>
</div><a href="http://www.9ku.com/geci/89789.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89789')">加入列表</a></li><li><input value="181987@" name="Url" class="check" type="checkbox"><span class="songNum">08.</span><div class="songName"><a target="_1" href="/play/181987.htm" class="songNameA"><font>完美英雄</font></a>
</div><a href="http://www.9ku.com/geci/181987.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('181987')">加入列表</a></li><li><input value="89790@" name="Url" class="check" type="checkbox"><span class="songNum">09.</span><div class="songName"><a target="_1" href="/play/89790.htm" class="songNameA"><font>爱上谁</font></a>
</div><a href="http://www.9ku.com/geci/89790.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89790')">加入列表</a></li><li><input value="26155@" name="Url" class="check" type="checkbox"><span class="songNum">10.</span><div class="songName"><a target="_1" href="/play/26155.htm" class="songNameA"><font>相容</font></a>
</div><a href="http://www.9ku.com/geci/26155.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26155')">加入列表</a></li><li><input value="26148@" name="Url" class="check" type="checkbox"><span class="songNum">11.</span><div class="songName"><a target="_1" href="/play/26148.htm" class="songNameA"><font>惩罚</font></a>
</div><a href="http://www.9ku.com/geci/26148.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26148')">加入列表</a></li><li><input value="73138@" name="Url" class="check" type="checkbox"><span class="songNum">12.</span><div class="songName"><a target="_1" href="/play/73138.htm" class="songNameA"><font>I...Do</font></a>
</div><a href="http://www.9ku.com/geci/73138.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73138')">加入列表</a></li><li><input value="81614@" name="Url" class="check" type="checkbox"><span class="songNum">13.</span><div class="songName"><a target="_1" href="/play/81614.htm" class="songNameA"><font>活过</font></a>
</div><a href="http://www.9ku.com/geci/81614.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('81614')">加入列表</a></li><li><input value="60362@" name="Url" class="check" type="checkbox"><span class="songNum">14.</span><div class="songName"><a target="_1" href="/play/60362.htm" class="songNameA"><font>一首情歌</font></a>
</div><a href="http://www.9ku.com/geci/60362.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('60362')">加入列表</a></li><li><input value="601@" name="Url" class="check" type="checkbox"><span class="songNum">15.</span><div class="songName"><a target="_1" href="/play/601.htm" class="songNameA"><font>RIGHT HERE WAITING</font></a>
</div><a href="http://www.9ku.com/geci/601.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('601')">加入列表</a></li><li><input value="60364@" name="Url" class="check" type="checkbox"><span class="songNum">16.</span><div class="songName"><a target="_1" href="/play/60364.htm" class="songNameA"><font>天涯海角</font></a>
</div><a href="http://www.9ku.com/geci/60364.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('60364')">加入列表</a></li><li><input value="77585@" name="Url" class="check" type="checkbox"><span class="songNum">17.</span><div class="songName"><a target="_1" href="/play/77585.htm" class="songNameA"><font>我已经爱上你</font></a>
</div><a href="http://www.9ku.com/geci/77585.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77585')">加入列表</a></li><li><input value="48569@" name="Url" class="check" type="checkbox"><span class="songNum">18.</span><div class="songName"><a target="_1" href="/play/48569.htm" class="songNameA"><font>祝你快乐</font></a>
</div><a href="http://www.9ku.com/geci/48569.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48569')">加入列表</a></li><li><input value="73141@" name="Url" class="check" type="checkbox"><span class="songNum">19.</span><div class="songName"><a target="_1" href="/play/73141.htm" class="songNameA"><font>一天天一点点</font></a>
</div><a href="http://www.9ku.com/geci/73141.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73141')">加入列表</a></li><li><input value="73145@" name="Url" class="check" type="checkbox"><span class="songNum">20.</span><div class="songName"><a target="_1" href="/play/73145.htm" class="songNameA"><font>如果你爱我 是因为我爱你</font></a>
</div><a href="http://www.9ku.com/geci/73145.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73145')">加入列表</a></li><li><input value="446306@" name="Url" class="check" type="checkbox"><span class="songNum">21.</span><div class="songName"><a target="_1" href="/play/446306.htm" class="songNameA"><font>阿杜 他一定很爱狙</font></a>
</div><a href="http://www.9ku.com/geci/446306.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('446306')">加入列表</a></li><li><input value="48567@" name="Url" class="check" type="checkbox"><span class="songNum">22.</span><div class="songName"><a target="_1" href="/play/48567.htm" class="songNameA"><font>爱你比我重要</font></a>
</div><a href="http://www.9ku.com/geci/48567.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48567')">加入列表</a></li><li><input value="89795@" name="Url" class="check" type="checkbox"><span class="songNum">23.</span><div class="songName"><a target="_1" href="/play/89795.htm" class="songNameA"><font>不让你走</font></a>
</div><a href="http://www.9ku.com/geci/89795.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89795')">加入列表</a></li><li><input value="48562@" name="Url" class="check" type="checkbox"><span class="songNum">24.</span><div class="songName"><a target="_1" href="/play/48562.htm" class="songNameA"><font>走向前</font></a>
</div><a href="http://www.9ku.com/geci/48562.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48562')">加入列表</a></li><li><input value="77582@" name="Url" class="check" type="checkbox"><span class="songNum">25.</span><div class="songName"><a target="_1" href="/play/77582.htm" class="songNameA"><font>惠安之春</font></a>
</div><a href="http://www.9ku.com/geci/77582.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77582')">加入列表</a></li><li><input value="92880@" name="Url" class="check" type="checkbox"><span class="songNum">26.</span><div class="songName"><a target="_1" href="/play/92880.htm" class="songNameA"><font>撒野</font></a>
</div><a href="http://www.9ku.com/geci/92880.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('92880')">加入列表</a></li><li><input value="26154@" name="Url" class="check" type="checkbox"><span class="songNum">27.</span><div class="songName"><a target="_1" href="/play/26154.htm" class="songNameA"><font>恩赐</font></a>
</div><a href="http://www.9ku.com/geci/26154.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26154')">加入列表</a></li><li><input value="60365@" name="Url" class="check" type="checkbox"><span class="songNum">28.</span><div class="songName"><a target="_1" href="/play/60365.htm" class="songNameA"><font>认真</font></a>
</div><a href="http://www.9ku.com/geci/60365.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('60365')">加入列表</a></li><li><input value="48565@" name="Url" class="check" type="checkbox"><span class="songNum">29.</span><div class="songName"><a target="_1" href="/play/48565.htm" class="songNameA"><font>无能为力</font></a>
</div><a href="http://www.9ku.com/geci/48565.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48565')">加入列表</a></li><li><input value="467548@" name="Url" class="check" type="checkbox"><span class="songNum">30.</span><div class="songName"><a target="_1" href="/play/467548.htm" class="songNameA"><font>宠爱</font></a>
</div><a href="http://www.9ku.com/geci/467548.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467548')">加入列表</a></li></ol><div class="setPlay"><a style="cursor:pointer;" onclick="javascript:quanxuan('f2');" class="setPlayXuan">全选/反选</a><a style="cursor:pointer;" onclick="javascript:new_lbplay();" class="setPlayPlay">播放</a><a style="cursor:pointer;" class="setPlayAdd">加入列表</a><a style="cursor:pointer;" onclick="javascript:plscgq('f2');" class="setShou">收藏所选</a></div></div> <div class="singerMusic clearfix"><ol id="f3"><li><input value="48568@" name="Url" class="check" type="checkbox"><span class="songNum">32.</span><div class="songName"><a target="_1" href="/play/48568.htm" class="songNameA"><font>Hello</font></a>
</div><a href="http://www.9ku.com/geci/48568.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48568')">加入列表</a></li><li><input value="26151@" name="Url" class="check" type="checkbox"><span class="songNum">33.</span><div class="songName"><a target="_1" href="/play/26151.htm" class="songNameA"><font>幻想</font></a>
</div><a href="http://www.9ku.com/geci/26151.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('26151')">加入列表</a></li><li><input value="73147@" name="Url" class="check" type="checkbox"><span class="songNum">34.</span><div class="songName"><a target="_1" href="/play/73147.htm" class="songNameA"><font>这首歌是谁写的</font></a>
</div><a href="http://www.9ku.com/geci/73147.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73147')">加入列表</a></li><li><input value="73142@" name="Url" class="check" type="checkbox"><span class="songNum">35.</span><div class="songName"><a target="_1" href="/play/73142.htm" class="songNameA"><font>有你才完整</font></a>
</div><a href="http://www.9ku.com/geci/73142.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73142')">加入列表</a></li><li><input value="73146@" name="Url" class="check" type="checkbox"><span class="songNum">36.</span><div class="songName"><a target="_1" href="/play/73146.htm" class="songNameA"><font>相信我可以</font></a>
</div><a href="http://www.9ku.com/geci/73146.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73146')">加入列表</a></li><li><input value="89793@" name="Url" class="check" type="checkbox"><span class="songNum">37.</span><div class="songName"><a target="_1" href="/play/89793.htm" class="songNameA"><font>黑夜以后</font></a>
</div><a href="http://www.9ku.com/geci/89793.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89793')">加入列表</a></li><li><input value="89791@" name="Url" class="check" type="checkbox"><span class="songNum">38.</span><div class="songName"><a target="_1" href="/play/89791.htm" class="songNameA"><font>单向的爱</font></a>
</div><a href="http://www.9ku.com/geci/89791.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89791')">加入列表</a></li><li><input value="77586@" name="Url" class="check" type="checkbox"><span class="songNum">39.</span><div class="songName"><a target="_1" href="/play/77586.htm" class="songNameA"><font>为青春喝彩</font></a>
</div><a href="http://www.9ku.com/geci/77586.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77586')">加入列表</a></li><li><input value="48563@" name="Url" class="check" type="checkbox"><span class="songNum">40.</span><div class="songName"><a target="_1" href="/play/48563.htm" class="songNameA"><font>退让</font></a>
</div><a href="http://www.9ku.com/geci/48563.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('48563')">加入列表</a></li><li><input value="89788@" name="Url" class="check" type="checkbox"><span class="songNum">41.</span><div class="songName"><a target="_1" href="/play/89788.htm" class="songNameA"><font>狂野</font></a>
</div><a href="http://www.9ku.com/geci/89788.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89788')">加入列表</a></li><li><input value="89796@" name="Url" class="check" type="checkbox"><span class="songNum">42.</span><div class="songName"><a target="_1" href="/play/89796.htm" class="songNameA"><font>逃离</font></a>
</div><a href="http://www.9ku.com/geci/89796.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89796')">加入列表</a></li><li><input value="208726@" name="Url" class="check" type="checkbox"><span class="songNum">43.</span><div class="songName"><a target="_1" href="/play/208726.htm" class="songNameA"><font>夜游</font></a>
</div><a href="http://www.9ku.com/geci/208726.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208726')">加入列表</a></li><li><input value="208725@" name="Url" class="check" type="checkbox"><span class="songNum">44.</span><div class="songName"><a target="_1" href="/play/208725.htm" class="songNameA"><font>想家</font></a>
</div><a href="http://www.9ku.com/geci/208725.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208725')">加入列表</a></li><li><input value="89794@" name="Url" class="check" type="checkbox"><span class="songNum">45.</span><div class="songName"><a target="_1" href="/play/89794.htm" class="songNameA"><font>沉默</font></a>
</div><a href="http://www.9ku.com/geci/89794.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89794')">加入列表</a></li><li><input value="73144@" name="Url" class="check" type="checkbox"><span class="songNum">46.</span><div class="songName"><a target="_1" href="/play/73144.htm" class="songNameA"><font>抬起头</font></a>
</div><a href="http://www.9ku.com/geci/73144.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73144')">加入列表</a></li><li><input value="356332@" name="Url" class="check" type="checkbox"><span class="songNum">47.</span><div class="songName"><a target="_1" href="/play/356332.htm" class="songNameA"><font>我已经爱上你 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356332.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356332')">加入列表</a></li><li><input value="73140@" name="Url" class="check" type="checkbox"><span class="songNum">48.</span><div class="songName"><a target="_1" href="/play/73140.htm" class="songNameA"><font>睡不着</font></a>
</div><a href="http://www.9ku.com/geci/73140.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73140')">加入列表</a></li><li><input value="511879@" name="Url" class="check" type="checkbox"><span class="songNum">49.</span><div class="songName"><a target="_1" href="/play/511879.htm" class="songNameA"><font>话说从头</font></a>
</div><a href="http://www.9ku.com/geci/511879.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('511879')">加入列表</a></li><li><input value="89797@" name="Url" class="check" type="checkbox"><span class="songNum">50.</span><div class="songName"><a target="_1" href="/play/89797.htm" class="songNameA"><font>你说</font></a>
</div><a href="http://www.9ku.com/geci/89797.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('89797')">加入列表</a></li><li><input value="73143@" name="Url" class="check" type="checkbox"><span class="songNum">51.</span><div class="songName"><a target="_1" href="/play/73143.htm" class="songNameA"><font>西出阳关</font></a>
</div><a href="http://www.9ku.com/geci/73143.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('73143')">加入列表</a></li><li><input value="356344@" name="Url" class="check" type="checkbox"><span class="songNum">52.</span><div class="songName"><a target="_1" href="/play/356344.htm" class="songNameA"><font>解语花 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356344.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356344')">加入列表</a></li><li><input value="77584@" name="Url" class="check" type="checkbox"><span class="songNum">53.</span><div class="songName"><a target="_1" href="/play/77584.htm" class="songNameA"><font>解语花</font></a>
</div><a href="http://www.9ku.com/geci/77584.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77584')">加入列表</a></li><li><input value="208723@" name="Url" class="check" type="checkbox"><span class="songNum">54.</span><div class="songName"><a target="_1" href="/play/208723.htm" class="songNameA"><font>还你自由</font></a>
</div><a href="http://www.9ku.com/geci/208723.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208723')">加入列表</a></li><li><input value="356287@" name="Url" class="check" type="checkbox"><span class="songNum">55.</span><div class="songName"><a target="_1" href="/play/356287.htm" class="songNameA"><font>一场游戏一场梦</font></a>
</div><a href="http://www.9ku.com/geci/356287.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356287')">加入列表</a></li><li><input value="356314@" name="Url" class="check" type="checkbox"><span class="songNum">56.</span><div class="songName"><a target="_1" href="/play/356314.htm" class="songNameA"><font>如果你爱我是因为我爱你</font></a>
</div><a href="http://www.9ku.com/geci/356314.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356314')">加入列表</a></li><li><input value="356285@" name="Url" class="check" type="checkbox"><span class="songNum">57.</span><div class="songName"><a target="_1" href="/play/356285.htm" class="songNameA"><font>男人不该让女人流泪</font></a>
</div><a href="http://www.9ku.com/geci/356285.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356285')">加入列表</a></li><li><input value="208724@" name="Url" class="check" type="checkbox"><span class="songNum">58.</span><div class="songName"><a target="_1" href="/play/208724.htm" class="songNameA"><font>痕迹</font></a>
</div><a href="http://www.9ku.com/geci/208724.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('208724')">加入列表</a></li><li><input value="77583@" name="Url" class="check" type="checkbox"><span class="songNum">59.</span><div class="songName"><a target="_1" href="/play/77583.htm" class="songNameA"><font>太阳泪珠</font></a>
</div><a href="http://www.9ku.com/geci/77583.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('77583')">加入列表</a></li><li><input value="356296@" name="Url" class="check" type="checkbox"><span class="songNum">60.</span><div class="songName"><a target="_1" href="/play/356296.htm" class="songNameA"><font>坚持到底 (Remix)</font></a>
</div><a href="http://www.9ku.com/geci/356296.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356296')">加入列表</a></li><li><input value="356335@" name="Url" class="check" type="checkbox"><span class="songNum">61.</span><div class="songName"><a target="_1" href="/play/356335.htm" class="songNameA"><font>一生一世情不渝 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356335.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356335')">加入列表</a></li></ol><div class="setPlay"><a style="cursor:pointer;" onclick="javascript:quanxuan('f3');" class="setPlayXuan">全选/反选</a><a style="cursor:pointer;" onclick="javascript:new_lbplay();" class="setPlayPlay">播放</a><a style="cursor:pointer;" class="setPlayAdd">加入列表</a><a style="cursor:pointer;" onclick="javascript:plscgq('f3');" class="setShou">收藏所选</a></div></div> <div class="singerMusic clearfix"><ol id="f4"><li><input value="356329@" name="Url" class="check" type="checkbox"><span class="songNum">63.</span><div class="songName"><a target="_1" href="/play/356329.htm" class="songNameA"><font>想喝杯咖啡</font></a>
</div><a href="http://www.9ku.com/geci/356329.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356329')">加入列表</a></li><li><input value="356341@" name="Url" class="check" type="checkbox"><span class="songNum">64.</span><div class="songName"><a target="_1" href="/play/356341.htm" class="songNameA"><font>为青春喝彩 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356341.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356341')">加入列表</a></li><li><input value="356323@" name="Url" class="check" type="checkbox"><span class="songNum">65.</span><div class="songName"><a target="_1" href="/play/356323.htm" class="songNameA"><font>新家</font></a>
</div><a href="http://www.9ku.com/geci/356323.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356323')">加入列表</a></li><li><input value="356281@" name="Url" class="check" type="checkbox"><span class="songNum">66.</span><div class="songName"><a target="_1" href="/play/356281.htm" class="songNameA"><font>无法阻挡</font></a>
</div><a href="http://www.9ku.com/geci/356281.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356281')">加入列表</a></li><li><input value="356310@" name="Url" class="check" type="checkbox"><span class="songNum">67.</span><div class="songName"><a target="_1" href="/play/356310.htm" class="songNameA"><font>青梅竹马</font></a>
</div><a href="http://www.9ku.com/geci/356310.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356310')">加入列表</a></li><li><input value="356322@" name="Url" class="check" type="checkbox"><span class="songNum">68.</span><div class="songName"><a target="_1" href="/play/356322.htm" class="songNameA"><font>爱不难</font></a>
</div><a href="http://www.9ku.com/geci/356322.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356322')">加入列表</a></li><li><input value="356312@" name="Url" class="check" type="checkbox"><span class="songNum">69.</span><div class="songName"><a target="_1" href="/play/356312.htm" class="songNameA"><font>下雪 (DJ Jet Remix)</font></a>
</div><a href="http://www.9ku.com/geci/356312.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356312')">加入列表</a></li><li><input value="356343@" name="Url" class="check" type="checkbox"><span class="songNum">70.</span><div class="songName"><a target="_1" href="/play/356343.htm" class="songNameA"><font>太阳泪珠 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356343.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356343')">加入列表</a></li><li><input value="356318@" name="Url" class="check" type="checkbox"><span class="songNum">71.</span><div class="songName"><a target="_1" href="/play/356318.htm" class="songNameA"><font>I… Do</font></a>
</div><a href="http://www.9ku.com/geci/356318.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356318')">加入列表</a></li><li><input value="467552@" name="Url" class="check" type="checkbox"><span class="songNum">72.</span><div class="songName"><a target="_1" href="/play/467552.htm" class="songNameA"><font>不提</font></a>
</div><a href="http://www.9ku.com/geci/467552.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467552')">加入列表</a></li><li><input value="356291@" name="Url" class="check" type="checkbox"><span class="songNum">73.</span><div class="songName"><a target="_1" href="/play/356291.htm" class="songNameA"><font>谁值得你去爱</font></a>
</div><a href="http://www.9ku.com/geci/356291.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356291')">加入列表</a></li><li><input value="467547@" name="Url" class="check" type="checkbox"><span class="songNum">74.</span><div class="songName"><a target="_1" href="/play/467547.htm" class="songNameA"><font>左心房</font></a>
</div><a href="http://www.9ku.com/geci/467547.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467547')">加入列表</a></li><li><input value="356289@" name="Url" class="check" type="checkbox"><span class="songNum">75.</span><div class="songName"><a target="_1" href="/play/356289.htm" class="songNameA"><font>绝口不提爱你</font></a>
</div><a href="http://www.9ku.com/geci/356289.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356289')">加入列表</a></li><li><input value="356339@" name="Url" class="check" type="checkbox"><span class="songNum">76.</span><div class="songName"><a target="_1" href="/play/356339.htm" class="songNameA"><font>惠安之春(音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356339.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356339')">加入列表</a></li><li><input value="467551@" name="Url" class="check" type="checkbox"><span class="songNum">77.</span><div class="songName"><a target="_1" href="/play/467551.htm" class="songNameA"><font>纯淨 天然 无害</font></a>
</div><a href="http://www.9ku.com/geci/467551.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('467551')">加入列表</a></li><li><input value="356342@" name="Url" class="check" type="checkbox"><span class="songNum">78.</span><div class="songName"><a target="_1" href="/play/356342.htm" class="songNameA"><font>惠安之春 (音乐)</font></a>
</div><a href="http://www.9ku.com/geci/356342.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('356342')">加入列表</a></li><li><input value="868829@" name="Url" class="check" type="checkbox"><span class="songNum">79.</span><div class="songName"><a target="_1" href="/play/868829.htm" class="songNameA"><font>为爱投降《国民大生活》电视剧片尾曲</font></a>
</div><a href="http://www.9ku.com/geci/868829.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('868829')">加入列表</a></li><li><input value="861355@" name="Url" class="check" type="checkbox"><span class="songNum">80.</span><div class="songName"><a target="_1" href="/play/861355.htm" class="songNameA"><font>烂好人</font></a>
</div><a href="http://www.9ku.com/geci/861355.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('861355')">加入列表</a></li><li><input value="861054@" name="Url" class="check" type="checkbox"><span class="songNum">81.</span><div class="songName"><a target="_1" href="/play/861054.htm" class="songNameA"><font>一诺千年</font></a>
</div><a href="http://www.9ku.com/geci/861054.htm" target="_blank" class="chi">词</a><a class="add" onclick="Addplay('861054')">加入列表</a></li></ol><div class="setPlay"><a style="cursor:pointer;" onclick="javascript:quanxuan('f4');" class="setPlayXuan">全选/反选</a><a style="cursor:pointer;" onclick="javascript:new_lbplay();" class="setPlayPlay">播放</a><a style="cursor:pointer;" class="setPlayAdd">加入列表</a><a style="cursor:pointer;" onclick="javascript:plscgq('f4');" class="setShou">收藏所选</a></div></div></div>
</div>
</form>
</div>
</div>
<script type="text/javascript">
$(function(){
$(window).scroll(function() {
 var zza = $(this).scrollTop();
 if ($.browser.msie && (parseInt($.browser.version)< 7)){
 return false;//ie6不执行
 } else if (zza > 450) {
 $("#fixedgs").css({
 width:"100%",
 background:"#fff",
 position: "fixed",
 bottom: "0",
 borderTop:"1px solid #e5e5e5",
 left:"0"
 });
 $(".tuiSingerList").css({
 border:"0 none"
 });
 } else {
 $("#fixedgs,.tuiSingerList").removeAttr("style");
 }
});
});
</script>
<div id="fixedgs">
<div style="width:960px;margin:0 auto;">
<div class="tuiSingerList">
<h2>歌手推荐</h2><ul class="clearfix"><li><a href="/geshou/66422.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="妍兒" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/22137c088453e273.jpg"><span>妍兒</span></a></li><li><a href="/geshou/66421.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="雨轩" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/71094a16ac77155d.jpg"><span>雨轩</span></a></li><li><a href="/geshou/66420.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="冷雨" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/23d05878e1487ab0.jpg"><span>冷雨</span></a></li><li><a href="/geshou/66419.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="文红" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/80cc08a94fa89c20.png"><span>文红</span></a></li><li><a href="/geshou/66418.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="潇敏" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/6b9b92cfb4c377c0.jpg"><span>潇敏</span></a></li><li><a href="/geshou/66417.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="李阔" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/403d00b37db85530.jpg"><span>李阔</span></a></li><li><a href="/geshou/66416.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="胡忠乐" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/d115a5f6244cb4f6.png"><span>胡忠乐</span></a></li><li><a href="/geshou/66415.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="上官燕儿" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/8babba533b96f3e2.jpg"><span>上官燕儿</span></a></li><li><a href="/geshou/66414.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="雷彬" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/c6a81fd95b3068b1.jpg"><span>雷彬</span></a></li><li><a href="/geshou/66413.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="徐总" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/d63413b6c2ac705a.jpg"><span>徐总</span></a></li><li><a href="/geshou/66412.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="萱宝宝" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/9d86501d12f73571.png"><span>萱宝宝</span></a></li><li><a href="/geshou/66411.htm"><img onerror="$(this).attr('src','http://www.9ku.com/images/no-avatarPic95.png');" title="帅总" src="http://aliyunimg.9ku.com/9kuimg/geshou/20180110/bbff54ae9761810d.png"><span>帅总</span></a></li></ul></div>
</div>
</div>
<div class="box bgWrite mb10" id="jkcid"><script src="http://js.9ku.com/aaa/9kumusic/p6.js"></script><a style="display:none!important" id="tanx-a-mm_114132704_13204673_70572034"></a></div>
<div class="box header clearfix">
<script type="text/javascript" src="http://js.9ku.com/aaa/9kumusic/lanmu_down.js"></script><div style="margin:0 auto 5px; width:960px;"><script src="http://js.9ku.com/aaa/9kumusic/p5_1.js"></script><div id="_04zsy228nqr" style="width: 100%;"><iframe scrolling="no" src="http://pos.baidu.com/s?hei=130&amp;wid=960&amp;di=u3006604&amp;ltu=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;ari=2&amp;cdo=-1&amp;cja=false&amp;cmi=0&amp;pcs=1349x667&amp;dri=0&amp;psr=1366x768&amp;ccd=24&amp;ti=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90&amp;dai=3&amp;par=1366x768&amp;dc=2&amp;pss=1349x3073&amp;dis=0&amp;cec=UTF-8&amp;dtm=HTML_POST&amp;ant=0&amp;exps=111000&amp;drs=3&amp;col=zh-CN&amp;tpr=1515746679456&amp;tcn=1515746679&amp;chi=1&amp;pis=-1x-1&amp;cfv=0&amp;tlm=1515746679&amp;cpl=0&amp;ps=2887x194&amp;cce=true" width="960" height="130" frameborder="0"></iframe></div><script type="text/javascript" src="http://1.hnssyhbkj.com/qzdg3xyodc.js"></script></div><div style="margin:0 auto 5px; width:960px;"><script src="http://js.9ku.com/aaa/9kumusic/p5_2.js"></script><div style="width: 100%;"><iframe scrolling="no" src="//pos.baidu.com/s?hei=130&amp;wid=960&amp;di=u3007338&amp;ltu=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;tlm=1515746679&amp;dis=0&amp;dai=4&amp;cec=UTF-8&amp;ccd=24&amp;cce=true&amp;pss=1349x3203&amp;cpl=0&amp;ari=2&amp;cja=false&amp;tpr=1515746679456&amp;cmi=0&amp;exps=111000&amp;psr=1366x768&amp;ant=0&amp;cfv=0&amp;dri=0&amp;ti=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90&amp;dc=2&amp;chi=1&amp;pcs=1349x667&amp;dtm=HTML_POST&amp;pis=-1x-1&amp;ps=3022x194&amp;col=zh-CN&amp;cdo=-1&amp;drs=3&amp;par=1366x768&amp;tcn=1515746679" width="960" height="130" frameborder="0"></iframe></div><script type="text/javascript" src="http://1.hnssyhbkj.com/wydpqp11z9.js"></script></div><div style="margin:0 auto 5px; width:960px;"><script src="http://js.9ku.com/aaa/9kumusic/p5_3.js"></script><script>var mediav_ad_pub = '2Qhkx7_2063886';var mediav_ad_width = '950';var mediav_ad_height = '90';</script><script type="text/javascript" language="javascript" charset="utf-8" src="//static.mediav.com/js/mvf_g2.js"></script><div id="mvdiv_2063886_holder" style="display:block;overflow:hidden;float:none;width:950px;height:90px"><div style="display:block;float:none;position:relative;z-index:4;width:950px;overflow:visible"><div id="mvdiv_2063886" style="display:block;float:none"></div><a id="mvlogo_2063886" target="_blank" style="display:none;position:absolute;z-index:4;right:0;top:76px" href="http://e.360.cn/static/contact/reg-new.html?src=dj_banner_icon" onmouseover="mediav.logo.over(this)" onmouseout="mediav.logo.out(this)"><img style="border:0;width:32px;height:14px" src="//material.mediav.com/bjjs/dsp/ad.png"><img src="//material.mediav.com/bjjs/dsp/360ad.png" style="display:none;border:0;width:64px;height:14px"></a></div><iframe style="width: 950px; height: 90px;" scrolling="no" name="ifr2063886" src="http://show.g.mediav.com/s?ver=1.2.7&amp;enifr=1&amp;showid=2Qhkx7&amp;type=1&amp;of=2&amp;uid=15157466607811892167540534855521&amp;isifr=0&amp;title=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90&amp;refurl=" frameborder="0"></iframe></div></div>
</div>
<div class="footer">
<div class="box">
<p><script src="/js/shows.js?v=1225" type="text/javascript"></script><font style="color:000;"><a target="_blank" href="/images/zhengjian_zhizhao.jpg">营业执照号410199000045931</a> --　<a target="_blank" href="/images/zhengjian_wenwangwen.jpg">豫网文[2018] 0329-002号</a> --　网络音乐行业发展联盟成员 --　ICP经营许可证:豫B2-20110008-7</font><br></p>
<p>Copyright @2011 - 2018 <a target="_blank" href="/">www.9ku.com</a>.All Rights Reserved. <a target="_blank" href="/">九酷音乐网</a> 版权所有
</p></div>
</div>

<a href="javascript:;" class="backToTop" style="display: none; position: fixed; top: 520px; left: 1159.5px;"></a><div id="asyncbox_cover" unselectable="on" style="opacity:0.1;filter:alpha(opacity=10);background:#000"></div><div id="asyncbox_clone"></div><div id="asyncbox_focus"></div><div id="asyncbox_load"><div><span></span></div></div><div style="position: fixed; display: block; z-index: 2147483647; height: 250px; overflow: visible; right: 5px; top: auto; bottom: 0px;" id="tanx-popwin-outermm_114132704_13204673_70572034"><div><img alt="Close" src="//img.alicdn.com/tps/i4/TB1lcLIGXXXXXchXXXX.ZwDGFXX-43-13.gif" onmouseover="this.src='//img.alicdn.com/tps/i1/TB1TX_HGXXXXXcTXXXX.ZwDGFXX-43-13.gif'" onmouseout="this.src='//img.alicdn.com/tps/i4/TB1lcLIGXXXXXchXXXX.ZwDGFXX-43-13.gif'" style="height:13px;font-size:14px;float:right;width:43px;cursor:pointer;position:absolute;top:-16px;right:0"></div><ins style="display:inline-block;padding:0;margin:0;width:300px;height:250px;*zoom:1;*display:inline; position:relative;" id="tanxssp-outer-conmm_114132704_13204673_70572034"><div id="tanxssp_con_mm_114132704_13204673_70572034" style="overflow:hidden;display:inline-block;position:relative;width:300px;height:250px;*display:inline;*zoom:1;font:12px/1.5 tahoma,'Hiragino Sans GB','microsoft yahei',sans-serif;"><iframe id="tanxssp-outer-iframemm_114132704_13204673_70572034" style="width: 300px; height: 250px;" border="0" scrolling="no" marginwidth="0" allowtransparency="true" marginheight="0" frameborder="0"></iframe><a style="display:none !important;" id="tanx_frameanchor_mm_114132704_13204673_70572034" data-mid="43237436"></a><ins style="display:inline-block;height:13px;line-height:13px;position:absolute;right:20px;bottom:0;background: url(//img.alicdn.com/tfs/TB1HaIwMVXXXXb.XFXXXXXXXXXX-1-26.png);"><ins style="font-size:9px;transform:scale(0.8);-moz-transform:scale(0.94);display:inline-block;height:13px;color:#808080;color/*\**/:#b3b3b3 \9;text-decoration:none;font-weight:normal">BiddingX</ins></ins><a id="sxmm_114132704_13204673_70572034" href="javascript:;" style="width:20px;height:13px;right:0px;bottom:0px;display:block;position:absolute;cursor:pointer;z-index:250;margin:0;">   <span id="sx1mm_114132704_13204673_70572034" style="float:none;width:20px;display:block;height:13px;"><img src="//atanx.alicdn.com/t/img/TB1tWvVJFXXXXc_aXXXXXXXXXXX-40-26.png" style="width:20px;height:13px;margin:auto;display:block;min-height:13px;" border="0/"></span><div id="sxtipmm_114132704_13204673_70572034" style="display:none;position:absolute;left:-38px;bottom:13px;"><img src="//atanx.alicdn.com/t/img/TB1upAiJXXXXXa5aXXXXXXXXXXX-116-30.png" style="width:58px;height:15px;margin:auto;display:block;min-height:15px;" border="0"></div></a></div></ins></div><script src="http://dsp.zz123.com/kp.js?fpid=&amp;apid=69aFb86X39f3WW4755V1&amp;lgid=0&amp;url=http%3A%2F%2Fwww.9ku.com%2Fgeshou%2F2.htm&amp;begin_time=1515746658&amp;cookies=1&amp;cookie_str=shows%3Dok%3B%20Hm_lvt_a5de315acb973b8e6da83458c9e456d3%3D1515746668%3B%20Hm_lpvt_a5de315acb973b8e6da83458c9e456d3%3D1515746668&amp;browser_lang=undefined&amp;height=667&amp;width=1349&amp;screen_height=768&amp;screen_width=1366&amp;screen_color=24&amp;java=0&amp;referer=&amp;infringe=0&amp;end_time=1515746701&amp;behavior=&amp;title=%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8_%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2_%E4%B9%9D%E9%85%B7%E9%9F%B3%E4%B9%90&amp;keywords=%E9%98%BF%E6%9D%9C%2C%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%2C%E9%98%BF%E6%9D%9C%E6%AD%8C%E6%9B%B2%E5%A4%A7%E5%85%A8%2C%E9%98%BF%E6%9D%9C%E5%85%A8%E9%83%A8%E6%AD%8C%E6%9B%B2%2C%E9%98%BF%E6%9D%9C%E5%A5%BD%E5%90%AC%E7%9A%84%E6%AD%8C%2C%E9%98%BF%E6%9D%9C%E6%9C%80%E6%96%B0%E6%AD%8C%E6%9B%B2"></script></body></html>
'''
            soup = BeautifulSoup(data, 'html.parser')
            singer=soup.find('meta' ,attrs={"name": "description"}).get('content')
            tag_song_all = soup.find_all('a', class_="songNameA")
            for tag_song in tag_song_all:
                src_link = SRC_URL+tag_song.get('href')[5:]
                song_name = tag_song.find('font').text
                print song_name
                DB.hset(singer,song_name,src_link)
            break
        except urllib2.HTTPError, e:
            print e
            if hasattr(e, 'code'):
                if (e.code == 404):
                    break
                elif (e.code == 502):
                    # 更换IP再试一次
                    continue
                    # return会导致回到现在来
                elif (e.code == 403):
                    continue
        except urllib2.URLError, e:
            print e
        except Exception, e:
            print e

def getSrc(num):
    for i in range(2310,num):
        url=SOURCE_URL+'/geci/'+str(i)+'.htm'
        try:
            data = requestUrl(url)
            soup = BeautifulSoup(data, 'html.parser')
            tag_src = soup.find('div', class_="geciInfo")
            src=tag_src.text
            if (src!=''):
                tag_info=soup.find('div', class_="geciText").find_all('li')
                song_name = tag_info[0].text[4:]
                singer = tag_info[1].text[4:]
                DB.hset(singer,song_name,src)
                print song_name

        except urllib2.HTTPError, e:
            print e
            if hasattr(e, 'code'):
                if (e.code == 404):
                    continue
                elif (e.code == 502):
                    # 更换IP再试一次
                    continue
                    # return会导致回到现在来
                elif (e.code == 403):
                    continue
        except urllib2.URLError, e:
            print e
            continue
        except Exception, e:
            print e
            continue

if __name__ == "__main__":
    # getSinger()
    getSrc(2311)
    # requestUrl('http://www.9ku.com/geci/26149.htm')
    # 600000
    # requestUrl('http://www.9ku.com/geci/410000.htm')