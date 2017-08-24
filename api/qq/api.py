import json
from html.parser import HTMLParser

from api import BaseAPI
from api.netease.config import header
from api.qq.config import *
from api.qq.models import *
from models import *


class QQMusicAPI(BaseAPI):
    """
    QQ音乐 api
    """

    def search_artists(self, content, page, num):
        pass

    def __init__(self,session, timeout=60, proxy=None, cookies=None):
        self.session = session
        self.timeout = timeout
        self.proxies = proxy
        self.session.cookies = cookies

    def get(self, url, params=None, headers=header, stream=False):
        """
        get 请求
        :param stream:
        :param url: 请求地址
        :param params: 参数
        :param headers: 请求头
        :return: 响应
        """
        resp = self.session.get(url, params=params, headers=headers, stream=stream)
        if resp.status_code == 200:
            return resp

    def post(self, url, data=None, headers=None):
        resp = self.session.post(url, data=data, headers=headers)

    def search(self, content, t, page, num=40):
        """
        搜索
        :param content: 搜索内容
        :param t: 搜索类型
        :param page: 页数
        :param num: 每页大小
        :return:请求结果
        """
        params = {
            'ct': '24',
            'qqmusic_ver': '1298',
            'remoteplace': 'txt.yqq.song',
            'searchid': '68035876895322363',
            'aggr': '1',
            'catZhida': '1',
            'lossless': '0',
            'flag_qc': '0',
            'g_tk': '5381',
            'jsonpCallback': 'searchCallbacksong593',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'jsonp',
            'inCharset': 'utf8',
            'outCharset': 'utf - 8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0',
            't': t,
            'p': page,
            'n': num,
            'w': content,
            'cr': '1',
            'new_json': '1',
        }
        resp = self.get(search_url, params).text
        resp = json.loads(resp[resp.index('(') + 1:resp.rindex(')')])
        return resp

    def search_songs(self, content, page=0, num=40):
        data = self.search(content, 0, page, num)
        code = data['code']
        if code == 0:
            list = data['data']['song']['list']
            songs = Songs()
            for i in list:
                song = Parse.parse_song(i)
                songs.append(song)
                # see paydownload
            return songs

    def get_key(self, mid, file):
        params = {
            'g_tk': '5381',
            'json': '3',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0',
            'cid': '205361747',
            'callback': 'callback',
            'uin': '0',
            'songmid': mid,
            'filename': file % mid,
            'guid': '534549750',
        }
        resp = self.get(key_url, params).text
        if isinstance(resp, str):
            resp = json.loads(resp[resp.index('(') + 1:resp.rindex(')')])
        return resp['data']['items'][0]['filename'], resp['data']['items'][0]['vkey']

    def song_url(self, song):
        file = 'M800%s.mp3' if song.pay == 0 else 'C400%s.m4a'
        file_name, vkey = self.get_key(song.mid, file)
        params = {'vkey': vkey, 'guid': '534549750', 'fromtag': '66', 'uin': '0'}
        url = play_url + file_name + '?'
        for p in params.keys():
            url += "%s=%s&" % (p, params[p])
        return url[:len(url) - 1]

    def lyric(self, song):
        params = {
            'nobase64': '1',
            'musicid': song.id,
            'callback': 'jsonp1',
            'g_tk': '5381',
            'jsonpCallback': 'jsonp1',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'jsonp',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq',
            'needNewCode': '0',
        }
        header = {
            'Referer': 'https://y.qq.com/n/yqq/song/%s.html' % song.mid
        }
        data = self.get(lyric_url, params, headers=header).text

        data = data[data.index('(') + 1:data.rindex(')')]
        data = json.loads(data)
        data = data['lyric']

        html_parser = HTMLParser()
        data = html_parser.unescape(data)
        return data

    def album_img_url(self, song):
        url = album_img_url % song.album.mid
        return url

    def playable(self, song):
        msginfo = {
            "1": "抱歉，该歌曲暂无法播放，可以试试其他歌曲",
            "10": "应版权方要求，暂不能分享此歌曲",
            "11": "应版权方要求不能免费下载，但如果是绿钻就没问题啦",
            "12": "版权方要求只有好歌曲赠送星钻用户和绿钻用户才能下载哦",
            "13": "应版权方要求不能免费播放，可付费后畅享",
            "14": "应版权方要求不能免费下载，可付费后畅享",
            "15": "应版权方要求不能免费播放，可升级QQ音乐新版后付费畅享",
            "16": "应版权方要求不能免费下载，可升级QQ音乐新版后付费畅享",
            "17": "开通包月服务，畅听更多歌曲",
            "18": "抱歉，应版权方要求，暂无法在当前国家或地区提供此歌曲服务",
            "19": "应版权方要求，暂不能收藏此歌曲",
            "2": "歌曲即将发布，关注歌手后我们第一时间告诉你",
            "20": "应版权方要求不能在线播放，可下载后播放",
            "21": "应版权方要求暂不能播放，不妨听听原曲吧",
            "22": "抱歉，该歌曲暂无音频资源，正努力寻找中",
            "23": "抱歉，应版权方要求，暂无法在当前国家或地区提供此歌曲服务",
            "24": "歌曲暂未上架，敬请期待！",
            "25": "歌曲暂未找到音频资源，欢迎提供资源至qqmusic155@tencent.com",
            "26": "该歌曲来自5sing音乐原创基地",
            "3": "应版权方要求暂不能播放，QQ音乐正玩命争取中:）",
            "4": "该歌曲来自第三方网站",
            "5": "抱歉，歌曲为其他设备导入，暂不支持播放哦",
            "6": "应版权方要求暂不能下载，先在线听听吧",
            "7": "应版权方要求暂不能播放，QQ音乐正玩命争取中:）",
            "8": "应版权方要求不能免费播放，如果是绿钻就没问题啦",
            "9": "应版权方要求购买后才能收听和下载哦，要不任性去音乐馆-专栏购买下"
        }
        if song.action == 0:
            return True
        else:
            logging.warning("%s:%s" % (str(song), msginfo[str(song.action)]))
            if song.action in [14]:
                return True
            return False
