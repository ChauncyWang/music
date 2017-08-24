var $loading = $('<img class="load_feed loading" src="http://img.xiami.net/res/img/default/loading2.gif" width="16" height="11" />');
var $loading2 = $('<img class="loading" src="http://img.xiami.net/res/img/default/loading2.gif" width="16" height="11" />');

var getBrowser = function() {
    var s = navigator.userAgent.toLowerCase();
    var a = new Array("msie", "firefox", "safari", "opera", "netscape");
    for (var i = 0; i < a.length; i++) {
        if (s.indexOf(a[i]) != -1) {
            return a[i];
        }
    }
    return "other";
};

var openShark = function(url) {
    var isMac = (navigator.userAgent.toLowerCase().indexOf("macintosh") != -1 || navigator.userAgent.toLowerCase().indexOf("mac os x") != -1),
        xmusicInstalled = false,
        softURL = '';
    if (!url) {
        url = 'emumo://';
    }
    try {
        var temp = document.getElementById('plugin0').valid;
        if (temp) {
            xmusicInstalled = true;
            delete temp;
        }
    } catch (e) {}
    if (isMac) {
        softURL = '/software/shark#mac';
        url = 'emumo://';
    } else {
        softURL = '/apps/win';
        if (!xmusicInstalled) {
            url = '';
        }
    }
    var popupStr = '<h3>提示</h3>\
                    <div class="dialog_content">\
                        <p class="alert">\
                            <iframe style="display:none;" src="' + url + '"></iframe>\
                            <span>客户端已启动，如未启动，请先安装虾米音乐客户端软件。</span>\
                            <a class="button major" href="' + softURL + '" target="_blank">安装客户端</a>\
                        </p>\
                    </div>\
                    <a class="Closeit" href="javascript:void(0);" title="关闭" onclick="closedialog();">关闭</a>';
    showDialog('', popupStr);
};

//弹窗
//ie6下高度的问题
var dialogbg = function() {
    if (getBrowser() == 'msie') {
        $('.dialog_sharp').height($('.dialog_main').height());
    }
};

function showDialog(url, ajaxText) {
    if (!$('.dialog_popup').length) {
        $('body').prepend('<div id="dialog_clt" class="dialog_popup"><div class="dialog_main"></div><div class="jqDrag"></div></div>');
    }
    if (!ajaxText) ajaxText = '<div class="dialog_content"><p class="loading">虾小米正为您在处理数据, 请稍候...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p></div><a href="" class="jqmClose">关闭</a>';
    if (!url) {
        $('.dialog_main').html(ajaxText);
    } else {
        url += (url.match(/\?/) ? "&" : "?") + "_xiamitoken=" + _xiamitoken;
    }
    $('.dialog_popup').jqm({
        ajax: url,
        modal: true,
        target: '.dialog_main',
        ajaxText: ajaxText,
        onLoad: function() {
            $('.dialog_popup').show().css({
                'margin-left': '-' + $('.dialog_main').width() / 2 + 'px',
                'margin-top': '-' + $('.dialog_main').height() / 2 + 'px'
            });
            /* hold for webkit render */
            setTimeout(function() {
                $('.dialog_popup').show().css({
                    'margin-left': '-' + $('.dialog_main').width() / 2 + 'px',
                    'margin-top': '-' + $('.dialog_main').height() / 2 + 'px'
                });
            }, 200);
        },
        onShow: function() {
            $('.dialog_popup').show().css({
                'margin-left': '-' + $('.dialog_main').width() / 2 + 'px',
                'margin-top': '-' + $('.dialog_main').height() / 2 + 'px'
            });
        },
        onHide: function() {
            $('.dialog_popup').css({
                'margin-left': '-130px',
                'margin-top': '-25px',
                'top': '50%',
                'left': '50%'
            }).hide();
            $('.jqmOverlay').hide();
        }
    }).jqDrag('.jqDrag').jqmShow();
}

function showAlert(url, ajaxText, jumpurl, doaction) {
    if (!$('.dialog_popup').length) {
        $('body').prepend('<div id="dialog_clt" class="dialog_popup"><div class="dialog_main"></div><div class="jqDrag"></div></div>');
    }
    if (!ajaxText) ajaxText = '<div class="dialog_content"><p class="loading">虾小米正为您在处理数据, 请稍候...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p></div><a href="" class="jqmClose">关闭</a>';
    if (!url) {
        $('.dialog_main').html('<h3>提示</h3><div class="dialog_content"><p class="alert"><span>' + ajaxText + '</span><a class="button major" href="' + jumpurl + '" onclick="' + doaction + '">确定</a></p></div><a href="" class="jqmClose">关闭</a>');
    } else {
        url += (url.match(/\?/) ? "&" : "?") + "_xiamitoken=" + _xiamitoken;
    }
    $('.dialog_popup').jqm({
        ajax: url,
        json: true,
        tmpl: '<h3>提示</h3><div class="dialog_content"><p class="alert"><span>${message}</span><a class="button major" href="${jumpurl}">确定</a></p></div><a href="" class="jqmClose">关闭</a>',
        modal: true,
        target: '.dialog_main',
        ajaxText: ajaxText,
        onShow: function() {
            $('.dialog_popup').show().css({
                'margin-left': '-' + $('.dialog_main').width() / 2 + 'px',
                'margin-top': '-' + $('.dialog_main').height() / 2 + 'px'
            });
        },
        onHide: function() {
            $('.jqmOverlay').hide();
            $('.dialog_popup').css({
                'margin-left': '-130px',
                'margin-top': '-25px',
                'top': '50%',
                'left': '50%'
            }).hide();
        }
    }).jqDrag('.jqDrag').jqmShow();
}

function closedialog() {
    $('.dialog_popup').jqmHide();
}



// 收藏
// 3，歌曲
// 4，歌单
// 5，专辑
// 6，艺人

function tag(id, type) {
    var url = '/music/tag/type/' + encodeURIComponent(type) + '/id/' + encodeURIComponent(id);
    showDialog(url);
}

// 专辑添加到歌单

function album2collect(id) {
    var url = '/song/collects/c/2/ids/' + encodeURIComponent(id);
    showDialog(url);
}

// 推荐
// 32，歌曲
// 33，专辑
// 34，艺人
// 35，歌单
// 36，歌曲评论
// 37，专辑评论
// 38，艺人评论
// 39，歌单评论
// 310， 小组话题
// 311，用户
// 312，小组

function recommend(id, type, sid) {
    var url = '/recommend/post';
    var url = url + '?object_id=' + encodeURIComponent(id) + "&type=" + encodeURIComponent(type) + "&t=" + 1000 * Math.random();
    if (sid) var url = url + '&sid=' + encodeURIComponent(sid);
    showDialog(url);
}
var getFlashVersion = function() {
    var nav = navigator,
        version = 0,
        flash;
    if (nav.plugins && nav.mimeTypes.length) {
        flash = navigator.plugins["Shockwave Flash"];
        if (flash) {
            version = flash.description.replace(/.*\s(\d+\.\d+).*/, "$1");
        }
    } else {
        try {
            flash = new window.ActiveXObject("ShockwaveFlash.ShockwaveFlash");
            if (flash) {
                version = flash.GetVariable("$version")
            }
        } catch (e) {}
    }
    if (version !== 0) {
        var fv = version.match(/\d+/g);
        if (fv.length > 0) {
            var v = fv.join('.')
            getFlashVersion = function() {
                return v
            };
            return v;
        }
    }
    return version;
};

function getInternetExplorerVersion() {
    var rv = -1,
        ua = navigator.userAgent;
    if (navigator.appName == 'Microsoft Internet Explorer') {
        var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat(RegExp.$1);
    } else if (navigator.appName == 'Netscape') {
        var re = new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat(RegExp.$1);
    }
    return rv;
}

function getOperaVersion() {
    var rv = -1,
        ua = navigator.userAgent;
    if (navigator.appName == 'Opera') {
        var re = new RegExp("Opera\/.*Version\/([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat(RegExp.$1);
    }
    return rv;
}
// 获取 flash core

function thisMovie(name) {
    var ie = getInternetExplorerVersion();
    if (ie != -1 && ie <= 9) {
        thisMovie = function(name) {
            return window[name];
        }
        return window[name];
    } else {
        thisMovie = function(name) {
            return document.getElementById(name);
        }
        return document.getElementById(name)
    }
};
/**
 * 统计打点
 */

function transclick(val, type) {
    var n = 'log_' + (new Date()).getTime();
    var url = 'http://www.xiami.com/blank.gif';
    var data = [
        'f=seiya',
        't=' + type,
        'fv=' + getFlashVersion(),
        'bm_an=' + navigator.appName,
        'v=' + val,
        '_=' + (new Date()).getTime()
    ];
    var req = window[n] = new Image();
    req.onload = req.onerror = function() {
        window[n] = null;
    };
    req.src = url + '?' + data.join('&')
    req = null;
};

function isIE() {
    return (navigator.appName == 'Microsoft Internet Explorer') || ((navigator.appName == 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null));
}

// 添加歌曲
function addSongs(str) {
    if (!isIE() && !!document.createElement('audio').canPlayType) {
        if ($.cookie('XMPLAYER_isOpen') != '1') {
            window.open('http://www.xiami.com/play?ids=' + str + '#open', 'xiamiMusicPlayer');
        }
        document.cookie = 'XMPLAYER_url='+ str +';path=/;domain=.xiami.com';
        document.cookie = 'XMPLAYER_addSongsToggler=1;path=/;domain=.xiami.com';
    }
    else {
        var playerTrigger = thisMovie('trans');
        if (typeof(playerTrigger.addSongs) === "function") {
            playerTrigger.addSongs(str);
            transclick(str, "add");
        } else {
            setTimeout(function() {
                if (typeof(playerTrigger.addSongs) === "function") {
                    playerTrigger.addSongs(str);
                    transclick(str, "add");
                } else {
                    openOldMusicPlayer(str);
                }
            }, 500);
        }        
    }
}

// 下载歌曲
function xm_download(id, type, ele) {
    if (!$.cookie('user')) {
      showDialog('/member/poplogin');
      return;
    }
    if (type && type == 'song') {
        var pare = ele.parentNode.parentNode.parentNode;
        if (pare) {
            var data = pare.getAttribute('data-json');
            data = JSON.parse(decodeURIComponent(data));
            data.id = id;
            // selectDownlodQuality(data);
            downloadToPC('song', id);
            return;
            var downloadstatus = pare.getAttribute('data-downloadstatus');
            if (downloadstatus) {
                if (downloadstatus == '0') {
                    checkSongPermission('download')
                    return;
                } else if (downloadstatus == '2') {
                    buyMusic('song', id, '下载');
                    return;
                }
            }
        }
    } else {
        var url = 'http://www.xiami.com/download/pay?id=' + encodeURIComponent(id);
        window.open(url);
    }
}
// 添加到

function collect(id) {
    var url = '/song/collect/id/' + encodeURIComponent(id);
    showDialog(url);
}
//type_name : collect , album

function play(song_id, type_name, type_id, ele) {
    if (!type_name) type_name = 'default';
    if (!type_id) type_id = 0;
    if (ele) {
        var pare = ele.parentNode.parentNode.parentNode;
        if (type_name == 'collect') {
            pare = pare.parentNode;
        }
        if (pare) {
            var playstatus = pare.getAttribute('data-playstatus');
            if (playstatus) {
                if (playstatus == '0') {
                    checkSongPermission('播放')
                    return;
                } else if (playstatus == '2') {
                    buyMusic('song', song_id, '播放');
                    return;
                }
            }
        }
    }
    addSongs(escape("/song/playlist/id/" + song_id + "/object_name/" + type_name + "/object_id/" + type_id));
}

// 播放专辑

function playalbum(album_id, me) {
    var needpay, playstatus, downloadstatus;

    if (me) {
        needpay = me.getAttribute('data-needpay'); // 0 不需要付费, 1 需要付费
        playstatus = me.getAttribute('data-playstatus'); // 0 不提供服务, 1 免费, 2 付费
        downloadstatus = me.getAttribute('data-downloadstatus'); // 0 不提供服务, 1 免费, 2 付费

        if (playstatus == '0') {
            checkAlbumPermission('play');
            return;
        }

        if (playstatus && playstatus == '2') {
            buyMusic('album', album_id, '播放');
            return;
        }
    }
    addSongs(escape('/song/playlist/id/' + album_id + '/type/1'));
}

// 播放歌单

function playcollect(list_id) {
    addSongs(escape("/song/playlist/id/" + list_id + "/type/3"));
}

// 播放每日歌单

function playdefault() {
    addSongs(escape('/song/playlist/id/1/type/9'));
}


// 播放未登录用户每日歌单

function playguestdaily() {
    addSongs(escape('/song/playlist/id/1/type/15'));
}

// 打开播放器
var playerDialog;

function openMusicPlayer(str) {
    //更改播放器高度 站外banner
    var reg = str.indexOf('out=1');
    if (reg != -1 && screen.height >= 640) {
        playerDialog = window.open("http://www.xiami.com/song/play?ids=" + str, "xiamiMusicPlayer", 'width=754,height=637');
        return;
    }
    transclick(str, 'open');
    var o = getOperaVersion(),
        i = getInternetExplorerVersion();
    if ((i == -1 || i > 6) && (o == -1 || o > 15)) {
        playerDialog = window.open("http://www.xiami.com/play?ids=" + str + "#open", "xiamiMusicPlayer");
    } else {
        //其他地方使用
        playerDialog = window.open("http://www.xiami.com/song/play?ids=" + str + "#open", "xiamiMusicPlayer", 'width=754,height=557');
    }
}

function openOldMusicPlayer(str) {
    transclick(str, 'openold');
    playerDialog = window.open("http://www.xiami.com/song/play?ids=" + str + "#open", "xiamiMusicPlayer", 'width=754,height=557');
}

function openPlayer(str) {
    var o = getOperaVersion(),
        i = getInternetExplorerVersion();
    if ((i == -1 || i > 6) && (o == -1 || o > 15)) {
        if (str.indexOf('uid=') === 0) {
            // 跟用户听
            playerDialog = window.open("http://www.xiami.com/play?" + str, "xiamiMusicPlayer");
        } else {
            playerDialog = window.open("http://www.xiami.com/play?ids=" + str, "xiamiMusicPlayer");
        }
    } else {
        if (str.indexOf('uid=') === 0) {
            // 跟用户听
            window.open("http://www.xiami.com/song/play?" + str, "xiamiMusicPlayer", 'scrollbars,width=720,height=645');
        } else {
            window.open("http://www.xiami.com/song/play?ids=" + str, "xiamiMusicPlayer", 'scrollbars,width=720,height=645');
        }
    }
};

// 选择所有

function selectAll(name) {
    var arr = $('input[name=' + name + ']');
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].disabled == false) {
            arr[i].checked = true;
        }
    }
}

// 反选

function inverse(name) {
    var arr = $('input[name=' + name + ']');
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].disabled == false) {
            arr[i].checked = !arr[i].checked;
        }
    }
}

// 获取选择项
function getSelectValues(name) {
    var sValue = '';
    var tmpels = $('input[name=' + name + ']');
    for (var i = 0, j = 0; i < tmpels.length; i++) {
        if (j == 100) break;
        if (tmpels[i].checked || (tmpels[i].type == 'hidden' && tmpels[i].defaultChecked)) {
            if (sValue == '') {
                sValue = tmpels[i].value;
            } else {
                sValue = sValue + "," + tmpels[i].value;
            }
            j++;
        }
    }
    return sValue;
};

function getSelectValues_2(name) {
    var sValue = '';
    var tmpels = $('input[name=' + name + ']');
    var alls = [];
    var downloads = [];
    for (var i = 0, j = 0; i < tmpels.length; i++) {
        if (j == 100) break;
        if (tmpels[i].checked || (tmpels[i].type == 'hidden' && tmpels[i].defaultChecked)) {
            var tr = tmpels.eq(i).parents('tr');
            var downloadstatus = tr.attr('data-downloadstatus');
            if (downloadstatus == 1) {
                if (sValue == '') {
                    sValue = tmpels[i].value;
                } else {
                    sValue = sValue + "," + tmpels[i].value;
                }
            } else {
                downloads.push(tmpels[i].value);
            }
            alls.push(tmpels[i].value);
            j++;
        }
    }
    if (downloads.length == 0) {
        if (sValue == '') {
            alert("没有资源可以下载！");return;
        }
        prepareZipx('song', sValue, '')
    } else {
        filterDownloadSong(alls.length, downloads.length, sValue);
    }
    //return sValue;
}

//3rd patry login
var referer = '';

var openWind = function(url) {
    var top = (document.body.clientHeight - 420) / 2;
    var left = (document.body.clientWidth - 520) / 2;
    window.open(url, 'connect_window', 'height=420, width=560, toolbar =no, menubar=no, scrollbars=yes, resizable=no,top=' + top + ',left=' + left + ', location=no, status=no');
};

var taoLogin = function() {
    // window.location.href = 'https://login.xiami.com/member/login?taobao=1';
    openWind('http://www.xiami.com/accounts/taobao-popup?done=' + referer);
};
var sinaLogin = function() {
    openWind('http://www.xiami.com/sina?referer=' + referer);
};
var qqLogin = function() {
    openWind('http://www.xiami.com/share/connect/type/qzone?referer=' + referer);
};
var renLogin = function() {
    openWind('/renren/goon?referer=' + referer);
};
var msnLogin = function() {
    openWind('/msnconnect');
};
var alipayLogin = function() {
    window.location.href = '/alipay';
};

//3rd patry reg
var taoReg = function() {
    location.href = '/member/login?taobao=1';
};
var sinaReg = function() {
    location.href = '/sina?xiamicallback=/member/weibologin/join/sina';
};
var qqReg = function() {
    location.href = '/share/connect/type/qzone?done=/member/weibologin/join/qzone';
};

function recommendLog(note, op, terminal, len, name, objectid, id, uid) {
    if (note) {
        uid = uid ? uid : 0;
        var url = 'http://www.xiami.com/recommend/log?';
        url = url + 'rec_note=' + encodeURIComponent(note) + '&op=' + op + '&terminal=' + encodeURIComponent(terminal) + '&playlen=' + encodeURIComponent(len) + '&object_name=' + encodeURIComponent(name) + '&' + objectid + '=' + id + '&userid=' + uid;
        $.ajax({
            type: "GET",
            url: url,
            dataType: "jsonp"
        });
    }
}

function buyMusic(type, id, action) {
    var url, ht, warm, typeName;

    if (location.href.match('idaily\.local\.xiami\.com') || location.href.match('gindis\.xiami\.com') || location.href.match('site\.local\.xiami\.com')) {
        url = 'http://im.local.xiami.com';
    } else {
        url = 'http://m.xiami.com';
    }
    typeName = '歌曲';
    if (type == 'album') {
        typeName = '专辑';
    }
    warm = '<p>对不起~暂时不支持网站购买，请使用<br/><a class="cf60" href="http://www.xiami.com/apps/mobile" target="_blank">虾米音乐APP</a>“扫一扫”功能扫描二维码购买' + typeName + '~</p>';

    // 购买URL
    if (type && id) {
        url += '/throne';
        if (type == 'album') {
            url += '?album_id=' + id;
        } else if (type == 'song') {
            url += '?song_id=' + id;
        } else {
            console.log('购买类别不存在');
        }
    }

    // 提示文案
    if (action) {
        if (type == 'album') {
            warm = '<p>抱歉，您需要支持歌手的数字专辑才可以' + action + '~</p><p>请使用<a class="cf60" href="http://www.xiami.com/apps/mobile" target="_blank">虾米音乐APP</a>“扫一扫”功能扫描二维码支付~</p>';
        } else if (type == 'song') {
            warm = '<p>抱歉，您需要先购买以后才可以' + action + '~<br/>请使用<a class="cf60" href="http://www.xiami.com/apps/mobile" target="_blank">虾米音乐APP</a>“扫一扫”功能扫描二维码支付~</p>';
        }
    }

    // 提示内容
    ht = '<style>.dialog_popup {width: 495px;}</style><h3>付费提示</h3>' +
        '<div class="dialog_content dialog-buy-music">' +
        '<div class="wram">' + warm + '</div>' +
        '<div class="qrcode"><img src="http://www.xiami.com/qrcode?u=' + url + '&w=200" /></div>' +
        '<div class="intro">说明：购买成功以后刷新页面即可使用~<br/>&nbsp;&nbsp;&nbsp;&nbsp;请确保app和网站账号统一~</div>' +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht)
}

function checkSongPermission(action) {
    var ht, warm;
    warm = '应版权方要求，歌曲暂不支持试听';

    if (action == 'download') {
        warm = '应版权方要求，歌曲暂不支持下载';
    } else if (action == 'all') {
        warm = '应版权方要求，没有歌曲可以播放'
    }
    ht = '<h3>温馨提示</h3>' +
        '<div class="dialog_content dialog-buy-music">' +
        '<div class="wram">' + warm + '</div>' +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);

    setTimeout(function() {
        closedialog();
    }, 2000);
}

function filterPlaySong(num, msg) {
    var ht, warm;
    warm = '应版权方要求，已过滤部分歌曲';

    if (msg) {
        warm = msg;
    }
    if (num && num != '') {
        warm = '应版权方要求，已过滤' + num + '首歌曲'
    }
    ht = '<h3>温馨提示</h3>' +
        '<div class="dialog_content dialog-buy-music">' +
        '<div class="wram">' + warm + '</div>' +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);

    setTimeout(function() {
        closedialog();
    }, 2000);
}

function filterDownloadSong(allNum, num, ids, msg) {
    var ht, warm, act;
    warm = '应唱片公司要求，已过滤部分歌曲';

    if (msg) {
        warm = msg;
    }
    if (num && num != '' && num != 0) {
        warm = '应唱片公司要求，已过滤' + num + '首歌曲'
    }

    if (allNum == num) {
        act = '';
        warm = '应唱片公司要求，所有歌曲都需要先单独付费购买才可以下载~'
    } else {
        act = '<div style="overflow:hidden;margin-top:10px;"><a class="bt_links" onclick="prepareZipx(\'song\', \'' + ids + '\', \'\')" style="color:#fff;    display: inline-block;float:none;" href="javascript:;" title=""><span>立即下载</span></a></div>'
    }

    ht = '<style>.dialog_popup {width: auto;}</style><h3>共' + (allNum - num) + '首，是否确认下载？</h3>' +
        '<div class="dialog_content dialog-buy-music">' +
        '<div class="wram">' + warm + '</div>' + act +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);

    // setTimeout(function() {
    //     closedialog();
    // }, 2000);
}

function checkAlbumPermission(action) {
    var ht, warm;
    warm = '应版权方要求，所有歌曲都需要先单独付费购买才可以试听~';

    if (action == 'download') {
        warm = '应版权方要求，所有歌曲都需要先单独付费购买才可以下载~';
    }
    ht = '<h3>温馨提示</h3>' +
        '<div class="dialog_content dialog-buy-music">' +
        '<div class="wram">' + warm + '</div>' +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);

    setTimeout(function() {
        closedialog();
    }, 2000);
}

function selectDownlodQuality(data) {
    var ht, warm, lowht, highht;
    //data = {low: "need_pay", HIGH: "need_pay", lossless: "no_permission"};
    if (data.LOW == 'FREE') {
        lowht = '<li style="cursor:pointer" onclick="prepareZipx(\'song\', ' + data.id + ', 1)" class="item"><span style="color:#f60;margin-right:5px;">⬇</span>流畅品质</li>';
    } else if (data.LOW == 'NEED_PAY') {
        lowht = '<li style="cursor:pointer" onclick="buyMusic(\'song\', ' + data.id + ', \'下载\');" class="item"><span style="color:#f60;margin-right:5px;">⬇</span><b class="identities ident-small">付费</b>流畅品质</li>'
    } else {
        lowht = '';
    }

    if (data.HIGH == 'FREE') {
        highht = '<li style="cursor:pointer" onclick="prepareZipx(\'song\', ' + data.id + ', 2)" class="item"><span style="color:#f60;margin-right:5px;">⬇</span>高品质</li>';
    } else if (data.HIGH == 'NEED_PAY') {
        highht = '<li style="cursor:pointer" onclick="buyMusic(\'song\', ' + data.id + ', \'下载\');" class="item"><span style="color:#f60;margin-right:5px;">⬇</span><b class="identities ident-small">付费</b>高品质</li>'
    } else {
        highht = '';
    }
    ht = '<h3>选择下载的品质</h3>' +
        '<div class="dialog_content dialog-downlod-music">' +
        '<ul class="cklist">' + lowht + highht + '</ul>' +
        '<div class="dialog_qrcode"><p>使用虾米音乐APP扫码离线到手机<em>荐</em></p><img src="http://www.xiami.com/qrcode?u=xiami%3A//song/' + data.id + '%3Faction%3Ddownload%26_referer%3Dpromotion%26_action%3Ddownload&w=110"></div>' +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);
}

function downloadToPC(type, id) {
    ht = '<h3>下载</h3>' +
        '<div class="dialog_content dialog-downlod-music">' +
        '<p style="font-size: 16px;color: #000;text-align: center;margin-top: 10px;">扫码使用虾米音乐App或PC客户端下载，享受高清音质</p>'+
        '<div class="dialog_qrcode"><img src="http://www.xiami.com/qrcode?u=xiami%3A//'+ type +'/' + id + '%3Faction%3Ddownload%26_referer%3Dpromotion%26_action%3Ddownload&w=110"><p>手机App下载</p></div>' +
        '<div class="dialog_pc">'+
        '<a class="major" href="http://www.xiami.com/apps/mobile" target="_blank">下载桌面端</a>'+
        // '<a class="minor" href="###">已安装桌面端，立即打开</a>'
        '</div></div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);
}

function GOODTip(html) {
    var ht, warm;
    ht = '<style>.dialog_popup {width: 300px;}</style><h3>提示</h3>' +
        '<div class="dialog_content dialog-login-music">' + html +
        '</div>' +
        '<a class="Closeit" onclick="closedialog();" title="" href="javascript:void(0);">关闭</a>';

    showDialog('', ht);
};

window.downloadHeartbeat = 0;
window.tipsLock = 0;
function prepareZipx(type, id, quality) {
    var self = this;
    //self._httpTab.removeClass('normal').addClass('prepare').find('em').text('mp3准备中');
    GOODTip('<div style="line-height:1.5">正在加载歌曲文件，<br/>请稍等，好了以后我们会为您自动下载</div>');
    var delay = setInterval(function() {
        var url = '/download/get-link';
        if (downloadHeartbeat > 0) {
            url = '/download/get-link?ping=1';
        }
        downloadHeartbeat ++;
        $.ajax({
            url: url,
            dataType: 'json',
            data: {
                type: type,
                id: id,
                quality: quality ? quality : ''
            },
            cache: false,
            success: function(data) {
                if (data.errorCode == 1 || data.errorCode == 999) {
                    clearInterval(delay);
                    downloadHeartbeat = 0;
                    GOODTip(data.errorMessage);
                    return;
                }
                if (!tipsLock) {
                    tipsLock = 1;
                    //GOODTip('<div style="line-height:1.5">正在加载歌曲文件，<br/>请稍等，好了以后我们会为您自动下载</div>');
                }
                if (data.errorCode == 0) {
                    if (data.url != '') {
                        clearInterval(delay);
                        tipsLock = 0;
                        downloadHeartbeat = 0;
                        $('body').append('<iframe style="display:none;" src="' + data.url + '"></iframe>');
                        //alert.html('如浏览器长时间无响应，点击<a href="'+data.url+'">这里重试</a>');
                    }
                } else {
                    clearInterval(delay);
                    downloadHeartbeat = 0;
                    tipsLock = 0;
                    //summary.removeClass('success').addClass('failure').find('i').text('下载失败！');
                    console.log(data.errorMessage);
                }
            },
            error: function() {
                alert('Load Error, please check your network');
            }
        });
    }, 2000);
    //closedialog();
}
// 统计

function stat(query) {
    (new Image()).src = 'http://www.xiami.com/statclick/?query=' + query;
}
