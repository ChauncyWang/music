import json
import logging

import re
import requests

from api import BaseAPI
from config import *
from netease.models import *
from netease.config import *
from netease.util import encrypted_request

from exception_handle import *
from http import cookiejar


class NeteaseAPI(BaseAPI):
    """
    网易云音乐 API
    """

    def __init__(self, session, timeout=60, proxy=None, cookies=None):
        self.session = session
        self.timeout = timeout
        self.proxies = proxy
        self.session.cookies = cookies

    @exception
    def post(self, url, data=None, headers=header):
        """
        对data 进行加密的 POST 请求
        :param url: post url
        :param data: post 的数据
        :param headers: post 请求的头
        :return: post 请求返回的信息
        """
        response = self.session.post(url, data=encrypted_request(data), headers=headers, proxies=self.proxies)
        if response.status_code == 200:
            return response
        else:
            raise RequestException(response.status_code)

    @exception
    def get(self, url, params=None, headers=header, stream=False):
        """
        Get 请求
        """
        response = self.session.get(url, params=params, headers=headers, proxies=self.proxies, stream=stream)
        if response.status_code == 200:
            return response
        else:
            raise RequestException(response.status_code)

    def search(self, content, _type, offset, limit=20):
        """
        进行搜索
        :param content: 要搜索的内容
        :param _type: 搜索类型
        :param offset: 偏移量
        :param limit:每页大小
        :return: json 数据类型的信息
        """
        params = {'s': content, 'type': _type, 'offset': offset,
                  'sub': 'false', 'limit': limit}
        return self.post(search_url, params)

    @exception
    def search_songs(self, content, offset=0, limit=20):
        """
        搜索歌曲
        :param content: 搜索内容
        :param offset: 偏移量
        :param limit:每页大小
        :return: 搜索到的 json 数据类型的歌曲信息
        """
        logging.info("搜索音乐:[搜索内容:%s, 偏移:%s, 页限制:%s]" % (content, offset, limit))
        result = json.loads(self.search(content, SearchType.song, offset, limit).text)
        if result['code'] == 200:
            result_songs = result['result']['songs']
            songs = []
            for s in result_songs:
                song = Parse.parse_song(s)
                song.url = self.song_url(song)
                songs.append(song)
            return songs
        else:
            raise ParameterException(result['code'], result['msg'])

    @exception
    def search_artists(self, content, offset=0, limit=40):
        """
        查询艺术家
        :param content: 要查询的内容
        :param offset: 位置偏移量
        :param limit: 查询的返回数量
        :return: 一个长度为 limit 的艺术家列表
        """
        result = json.loads(self.search(content, SearchType.artist, offset, limit).text)
        if result['code'] == 200:
            return NArtists(result['result']['artists'])
        else:
            raise ParameterException(result['code'], result['msg'])

    @exception
    def search_albums(self, content, offset=0, limit=40):
        result = json.loads(self.search(content, SearchType.album, offset, limit).text)
        if result['code'] == 200:
            r = []
            result = result['result']['albums']
            for t in result:
                r.append(NAlbum(t))
            return r
        else:
            raise ParameterException(result['code'], result['msg'])

    @exception
    def get_song_url(self, _id, br=320000):
        """
        根据歌曲id获取播放链接
        :param _id:歌曲id
        :param br:歌曲品质
        :return:歌曲链接
        """
        params = {'ids': [_id], 'br': br, 'csrf_token': ''}
        response = self.post(song_url, params)
        response = json.loads(response.text)
        return response['data'][0]['url']

    @exception
    def get_songs_url(self, ids, br=320000):
        """
        根据歌曲列表获取列表内歌曲的链接
        :param ids: 歌曲 id 列表
        :param br:歌曲品质
        :return: 链接列表
        """
        params = {'ids': ids, 'br': br, 'csrf_token': ''}
        response = self.post(song_url, params)
        response = json.loads(response.text)
        result = []
        for song in response['data']:
            result.append(song['url'])
        return result

    @exception
    def get_toplist(self):
        """
        获取各个榜单的信息
        :return:榜单列表
        """
        ret = []
        result = self.get(toplist_url).text
        patt = r'<h2 class=".*?f-ff1"?>(.*?)</h2>\s*<ul class="f-cb">([\s\S]*?)</ul>'
        for i in re.findall(patt, result):
            dic = {'title': i[0], 'toplist': []}
            patt = r'<a class="avatar" href=".*?id=(.*?)">\s*?<img src="(.*?)"\s*?alt="(.*?)"/>'
            l = re.findall(patt, i[1])
            for j in l:
                subs = {'id': j[0], 'img_url': j[1], 'name': j[2]}
                dic['toplist'].append(subs)
            ret.append(dic)
        return ret

    @exception
    def get_toplist_songs(self, toplist_id):
        """
        根据榜单 id 获取榜单所拥有的歌曲
        :param toplist_id: 榜单 id
        :return: 歌单
        """
        resp = self.get(toplist_url, {'id': toplist_id}).text
        patt = '<textarea style="display:none;">(.*?)</textarea>'
        result = json.loads(re.search(patt, resp).group(1))
        for i in result:
            s = NSong(i)

    @exception
    def album_img_url(self, song):
        return song.album.pic_url

    def playable(self, song):
        return song.url is not None

    @exception
    def lyric(self, song):
        """
        获取歌词
        :param song:要获取歌词的歌曲
        :return: 歌曲歌词
        """
        params = {'id': song.id, 'lv': -1, 'kv': -1, 'tv': -1}
        result = self.get(lyric_url, params)
        result = json.loads(result.text)
        try:
            return result['lrc']['lyric']
        except KeyError as e:
            e.with_traceback()
            return None

    @exception
    def song_url(self, song):
        """
        获取歌曲 url
        :param song: 要获取的歌曲
        :return: 歌曲播放地址
        """
        br = 320000
        params = {'ids': [song.id], 'br': br, 'csrf_token': ''}
        response = self.post(song_url, params)
        response = json.loads(response.text)
        return response['data'][0]['url']
