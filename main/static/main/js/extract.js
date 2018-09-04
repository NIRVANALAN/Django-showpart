var packJson = {
    name: 'Larry',
    password: '123'
}
var arrayJson = [{
    name: 'Liza',
    password: '123'
},
    {
        name: 'Mike',
        password: '456'
    }
];

// for ( var i in arrayJson ) {
//     alert( arrayJson[i].name)
// }
// $.getJSON( './test.json', function ( data ) {
//     alert( data )
// } )
// var Ajax = function () {
//   $.getJSON('test.json', function (data) {
//     $.each(data, function (i, item) {
//       $('#disp').append('<h3>' + item.name + '</h3>')
//       $('#disp').append('<p>' + item.sex + '</p>')
//       $('#disp').append('<p>' + item.email + '</p>')
//     })
//   })
// }
var info = [];
function extractInfo() {
    // function camerasInfo(name,x,y,id){
    //     this.name = name;
    //     this.x = x;
    //     this.y = y;
    //     this.id = id;
    // }

    $.getJSON('./main/static/main/js/info.json', function (data) {
        // info = data;
        // info = $.extend(true, [], data["camera"]);
        $.each(data["camera"], function (i, item) {
            $('#disp').append('<h3>' + item.name + '</h3>');
            $('#disp').append('x:' + item.x);
            $('#disp').append(' y:' + item.y);
            $('#disp').append(' id:' + item.id + '<hr>');
            // var camera = new camerasInfo(item.name,item.x,item.y,item.id);
            // var camera = {name:item.name,x:item.x,y:item.y,id:item.id};
            // info.push(camera);
        })
    });
    return info;
}

$(function () {
    $('#btn').click(function () {
        // 注意,这里面的路径是URL,UAG是在localhost下做的测试.
        $.getJSON('js/userinfo.json', function (data) {
            var $jsontip = $('#jsonTip')
            var strHtml = null // 存储数据的变量
            $jsontip.empty() // 清空内容
            $.each(data, function (infoIndex, info) {
                strHtml += '姓名：' + info['name'] + '<br>'
                strHtml += '性别：' + info['sex'] + '<br>'
                strHtml += '邮箱：' + info['email'] + '<br>'
                strHtml += '<hr>'
            })
            $jsontip.html(strHtml) // 显示处理后的数据
        })
    })
});

function extractCameraInfo() {
    var camera_info = [];
    $.ajaxSettings.async = false;
    $.getJSON('js/info.json', function (result) {
        $.each(result["camera"], function (index, info) {
            camera_info.push(info);
        })
    });
    return camera_info;
}

var ratio = 100;

function isRealNum(val) {
    // isNaN()函数 把空串 空格 以及NUll 按照0来处理 所以先去除
    if (val === "" || val == null) {
        return false;
    }
    if (!isNaN(val)) {
        return true;
    } else {
        return false;
    }
}

function extractDotTrace() {

    var camera_info = extractCameraInfo();
    var dotbook = [];
    var frame_points = [];
    var max = 0;

    $.getJSON('<STATIC_PATH>/js/visudata_dotbook.json', function (data) {
        var width = 840;
        var height = 600;
        for (var p in data) {
            // alert("data[119][2]:"+ data[ "119" ][ "2" ] );
            let points = [];
            for (var i in data[p]) {
                // alert(p+" "+i+":"+data[p][i])
                max = Math.max(max, data[p][i]);
                var point = {x: camera_info[i - 1].x * ratio, y: camera_info[i - 1].y * ratio, value: data[p][i]};
                points.push(point);
            }
            frame_points.push(points);
        }
    });
    return {max: max, data: frame_points};
}

function extractPathTrace() {
    dot_data = extractDotTrace();
    var camera_info = extractCameraInfo();
    var path_points = [];
    var max = dot_data.max;
    var number = 0;
    var tmp;
    var path_debug = [];

    $.getJSON('js/visudata_pathbook.json', function (data) {
        // alert(data[1302]['(\'2\', \'5\')']);
        // alert(data[10000]['(\'4\', \'6\')']);
        for (var p in data) {
            number = p;
            let beg = 0;
            let end = 0;
            var points = [];
            let debug = [];
            for (var i in data[p]) {
                tmp = i;
                // max = Math.max(max,data[p][i]);
                //"('1', '4')"
                debug.push(data[p][i]);
                var line_points = [];
                beg = parseInt(i.slice(2, 3));
                end = parseInt(i.slice(7, 8));
                if (!isRealNum(beg) || !isRealNum(end)) {
                    break;
                }
                dist_x = Math.abs(camera_info[beg - 1].x - camera_info[end - 1].x);
                max = Math.max(max, data[p][i]);
                //('6', '')
                dist_y = Math.abs(camera_info[beg - 1].y - camera_info[end - 1].y);
                var dist = Math.sqrt(Math.pow(dist_x, 2) + Math.pow(dist_y, 2)) * ratio;
                var iter = dist;
                while (iter > 0) {
                    var point = {
                        x: (camera_info[beg - 1].x + iter / dist * dist_x) * ratio,
                        y: (camera_info[beg - 1].y + iter / dist * dist_y) * ratio,
                        value: data[p][i]
                    };
                    // line_points.push(point);
                    dot_data.data[p].push(point);
                    iter-=10;
                }
                // points.push(line_points);
                // alert(data[p][i]);
            }
            // path_debug.push(debug);
            if (!(line_points == null)) {
                points.push(line_points);
            }
            path_points.push(points);
            points = [];
        }
    });
    var bind_points = [];
    let i = 0;
    // while (i < path_points.length) {
    //     bind_points[i] = dot_data.data[i].concat(path_points[i]);
    //     i++;
    // }
    return {max: max, data: dot_data.data}
    //max:5   data_len:55300
}

window.onload = function () {

    function generateRandomData(len) {
        var points = [];
        var max = 0;
        var width = 840;
        var height = 400;
        while (len--) {
            var val = Math.floor(Math.random() * 100);
            max = Math.max(max, val);
            var point = {x: Math.floor(Math.random() * width), y: Math.floor(Math.random() * height), value: val};
            points.push(point);
        }
        return {max: max, data: points};
    }

    function $(selector) {
        return document.querySelectorAll(selector);
    }

    function AnimationPlayer(options) {
        this.heatmap = options.heatmap;
        this.data = options.data;
        this.interval = null;
        this.animationSpeed = options.animationSpeed || 300;
        this.wrapperEl = options.wrapperEl;
        this.isPlaying = false;
        this.init();
    };
    var max_len = 30;
    AnimationPlayer.prototype = {
        init: function () {
            var dataLen = this.data.length;
            this.wrapperEl.innerHTML = '';
            var playButton = this.playButton = document.createElement('button');
            playButton.onclick = function () {
                if (this.isPlaying) {
                    this.stop();
                } else {
                    this.play();
                }
                this.isPlaying = !this.isPlaying;
            }.bind(this);
            playButton.innerText = 'play';
            this.wrapperEl.appendChild(playButton);

            var events = document.createElement('div');
            events.className = 'heatmap-timeline';
            events.innerHTML = '<div class="line"></div>';
            for (var i = 0; i < max_len; i++) {
                var xOffset = 100 / (max_len - 1) * i;
                var ev = document.createElement('div');
                ev.className = 'time-point';
                ev.style.left = xOffset + '%';
                ev.onclick = (function (i) {
                    return function () {
                        this.isPlaying = false;
                        this.stop();
                        this.setFrame(Math.floor(i * dataLen / max_len));
                    }.bind(this);
                }.bind(this))(i);
                events.appendChild(ev);
            }
            this.wrapperEl.appendChild(events);
            this.setFrame(0);
        }, play: function () {
            var dataLen = this.data.length;
            this.playButton.innerText = 'pause';
            this.interval = setInterval(function () {
                this.setFrame(++this.currentFrame % dataLen);
            }.bind(this), this.animationSpeed);
        }, stop: function () {
            clearInterval(this.interval);
            this.playButton.innerText = 'play';
        }, setFrame: function (frame) {
            this.currentFrame = frame;
            // if (frame%10===0){
            //     alert("currentFrame:"+frame);
            // }
            x = document.getElementById("frame");
            x.innerHTML = frame;
            var snapshot = this.data[frame];
            this.heatmap.setData(snapshot);
            var timePoints = $('.heatmap-timeline .time-point');
            for (var i = 0; i < timePoints.length; i++) {
                timePoints[i].classList.remove('active');
            }
            timePoints[frame % timePoints.length].classList.add('active');
        }, setAnimationData: function (data) {
            this.isPlaying = false;
            this.stop();
            this.data = data;
            this.init();
        }, setAnimationSpeed: function (speed) {
            this.isPlaying = false;
            this.stop();
            this.animationSpeed = speed;
        }
    };
    var heatmapInstance = h337.create(
        {
            container: document.querySelector('.heatmap'),
            // radius:20,
            backgroundColor: 'rgba(0.5,0.5,0.5,.95)',
            // gradient: {
            //     // enter n keys between 0 and 1 here
            //     // for gradient color customization
            //     '.5': 'blue',
            //     '.8': 'red',
            //     '.95': 'white'
            // },
            maxOpacity: .9,
            // minimum opacity. any value > 0 will produce
            // no transparent gradient transition
            minOpacity: .3
        }
    );
    var animationData = [];
    // for (var i = 0; i < 20; i++) {
    //     animationData.push(generateRandomData(300));
    // }
    pathbook_info = extractPathTrace();

    for (var i = 0; i < dot_data.data.length; i++) {
        animationData.push({max: pathbook_info.max, data: pathbook_info.data[i]})
    }
    var player = new AnimationPlayer({
        heatmap: heatmapInstance,
        wrapperEl: document.querySelector('.timeline-wrapper'),
        data: animationData,
        animationSpeed: 500
    });
    var controlButtons = $('.trigger-refresh');
    for (var i = 0; i < controlButtons.length; i++) {
        controlButtons[i].onclick = function () {
            var fps = this.dataset.fps;
            player.setAnimationSpeed(1 / (+fps) * 1000);
        };
    }
    var getPiwik = (function () {
        var piwik;
        return function () {
            if (piwik) {
                return piwik;
            } else {
                if (!window.Piwik) {
                    piwik = {
                        getAsyncTracker: function () {
                            return {
                                trackEvent: function () {
                                    return;
                                }
                            }
                        }
                    };
                } else {
                    piwik = window.Piwik;
                }
                return piwik;
            }
        };
    })();
};
