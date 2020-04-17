import re 
a="http://wsdx.nwafu.edu.cn/ybdy/lesson/play?v_id=2066&r_id=4940&r=video&pg="
v_id=re.findall('v_id=(.*?)&',a)[0]
r_id=re.findall('r_id=(.*?)&',a)[0]
print(r_id)

html='''
    $(".video_lists").animate({scrollTop: $(".video_red1").offset().top - 162}, 1000);

    var timer = "";

    // 续播定时器
    function current_time() {
        timer = setInterval(function () {
            $.ajax({
                type: "POST",
                cache: false,
                dataType: "json",
                url: "/ybdy/lesson/current_time",
                data: {
                    rid: "4940",
                    time: players[0].getCurrentTime(),
                    _xsrf: $(":input[name='_xsrf']").val()
                },
                success: function () {
                }
            });
        }, 30000);
    }

    var loop_flag = "";

            var players = plyr.setup({
                keyboardShortcuts: {focused: false, global: false, pause: false},
                tooltips: {controls: false, seek: false},
                seek: false,
                preload: "load",
                seekTime: 0
                //controls: ['play-large', 'play', 'current-time', 'duration', 'mute', 'volume', 'captions']
            });


    players[0].on('ended', function (event) {
        if ("video" == "video") {
            clearInterval(timer);   //定时器清除；
        }

        $.ajax({
            type: "POST",
            cache: false,
            dataType: "json",
            url: "/ybdy/lesson/resource_record",
            data: {
                rid: "1364978",
                resource_id: "4940",
                video_id: "2066",
                lesson_id: "208",
                _xsrf: $(":input[name='_xsrf']").val()
            },
            success: function (data) {
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
    });

    // 监听播放事件
    players[0].on('play', function (event) {
        studyTime();

        if ("video" == "video") {
            current_time();
        }

    });

    // 监听暂停事件
    players[0].on('pause', function (event) {
        window.clearTimeout(flag);
        if ("video" == "video") {
            clearInterval(timer);   //定时器清除；
        }
    });

    // 定期暂停方法
    function loop_pause() {
        players[0].pause();

        public_alert(1, ["继续"], '<i class="iconfont">&#xe633;</i><p>视频已暂停，点击按钮后继续学习！</p><p></p>', 'public_cont1', function () {
            $(".public_close").click(); //此为关闭方法
            players[0].play();
        });
    };

    document.addEventListener('visibilitychange', function () { //浏览器切换事件
        if (document.visibilityState == 'hidden') {
            players[0].pause();
        } else {
            players[0].on('loadedmetadata', function (event) {
                players[0].play()
            })
        }
    });'''
p_data=re.findall('_record",data:{(.*)_xsrf',html.replace('\n','').replace('\t','').replace(" ",""))[0]
rid=re.findall('rid:"(.*?)"',p_data)[0]
lesson_id=re.findall('lesson_id:"(.*?)"',p_data)[0]
print(rid,lesson_id)