# -*- coding: utf-8 -*- #
TEMP_FILE='temp.txt'
TIME_SLEEP=4
Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    ,'Referer':'http://music.163.com/user/fans?id=97526496'


}
M_Headers={
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host':'music.163.com',
    'Origin':'http://music.163.com',
    'Cookie':'appver=1.5.0.75771;',
    'Referer':'http://music.163.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
SOURCE_URL='http://www.9ku.com'
SRC_URL='http://www.9ku.com/geci'
SONG_NAME='songname'
SONG_LINK='songlink'
COMBINE='combine'
OUSER='combine'
CUSER='combine'
SONGS='songs'
USER='user'
LIKE_SONGS='like_songs'

FILE_OFFSET=-7


HTML_HEAD='''<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
</head>
<body>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main" style="height:1100px"></div>
    <!-- ECharts单文件引入 -->
    <script src="http://echarts.baidu.com/build/dist/echarts.js"></script>
    <script type="text/javascript">
        // 路径配置
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });

        // 使用
        require(
            [
                'echarts',
                'echarts/chart/bar', // 使用柱状图就加载bar模块，按需加载
                'echarts/chart/force'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('main'));

                var option = {
    title : {
        text: '网易云用户关系图',
        subtext: '百级数据',
        x:'right',
        y:'bottom'
    },
    tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}'
    },
    toolbox: {
        show : true,
        feature : {
            restore : {show: true},
            magicType: {show: true, type: ['force', 'chord']},
            saveAsImage : {show: true}
        }
    },
    legend: {
        x: 'left',
        data:['家人','朋友','人物']
    },
    series : [
        {
            type:'force',
            name : "人物关系",
            ribbonType: false,
            categories : [
                {
                    name: '人物'
                },
                {
                    name: '家人'
                },
                {
                    name:'朋友'
                }
            ],
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        textStyle: {
                            color: '#333',
                            fontWeight:'bolder',
                            fontSize:'25'
                        }
                    },
                    nodeStyle : {
                        brushType : 'both',
                        borderColor : 'rgba(255,215,0,0.4)',
                        borderWidth : 3
                    },
                    linkStyle: {
                        type: 'curve'
                    }
                },
                emphasis: {
                    label: {
                        show: false
                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                    },
                    nodeStyle : {
//                        r: 30
                    },
                    linkStyle : {}
                }
            },
            useWorker: false,
            minRadius : 15,
            maxRadius : 60,
            gravity: 1.1,
            scaling: 1.1,
            roam: 'move',
            nodes:[
'''
HTML_MIDDLE='''
],
            links : ['''
HTML_END='''
]
        }
    ]
};

                // 为echarts对象加载数据
                myChart.setOption(option);
            }
        );
    </script>
</body>

'''