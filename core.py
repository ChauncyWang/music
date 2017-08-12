import hashlib
import logging
import os
from contextlib import closing
from threading import Thread

import config, qq, netease
from netease import NETEASE
from netease.api import NeteaseAPI
from netease.models import NSong, NAlbum
from qq import QQ
from qq.api import QQMusicAPI
from qq.models import QSong, Album, QAlbum


class Core:
    """ 搜索核心 """

    def __init__(self):
        self.qq = QQMusicAPI()
        self.netease = NeteaseAPI()
        self.use_qq = False
        self.use_netease = False
        self.use_api(qq.QQ | netease.NETEASE)

    def use_api(self, x):
        """ 设置搜索使用的 api """
        if x & qq.QQ:
            logging.info("使用QQ音乐API...")
            self.use_qq = True
        if x & netease.NETEASE:
            logging.info("使用网易云音乐API...")
            self.use_netease = True

    def search(self, content, page, num):
        """
        双引擎搜索
        :param content: 搜索内容
        :param page: 页数
        :param num: 每页大小
        :return: 歌曲列表
        """
        result = []
        result_qq = []
        result_netease = []
        if self.use_qq:
            result_qq = self.qq.search_songs(content, page, num)
        if self.use_netease:
            result_netease = self.netease.search_songs(content, num * page, num)

        for nsong in result_netease:
            for qsong in result_qq:
                if qsong == nsong:
                    result.append(SONG.merger_song(qsong, nsong))
                    break
        for song in result:
            result_qq.remove(song)
            result_netease.remove(song)
        result += result_qq
        result += result_netease
        return result

    def playable(self, song):
        """ 是否能播放 """
        re = 0
        if isinstance(song, QSong) and self.qq.playable(song):
            re |= QQ
        if isinstance(song, NSong) and self.netease.playable(song):
            re |= NETEASE
        return re

    def song_url(self, song, use_qq):
        if use_qq:
            return self.qq.song_url(song)
        else:
            return self.netease.song_url(song)

    def lyric(self, song, use_qq):
        if use_qq:
            return self.qq.lyric(song)
        else:
            return self.netease.lyric(song)

    def album_img_url(self, song, use_qq):
        if use_qq:
            return self.qq.album_img_url(song)
        else:
            return self.netease.album_img_url(song)


class DownloadThread(Thread):
    """ 下载线程 """

    def __init__(self, session, url, path, file_name, update_callback, finished_callback, chunk_size=1024 * 100):
        """
        :param session: http请求的会话，某些请求可能需要cookie
        :param url: 请求地址
        :param path: 文件保存路径
        :param file_name: 文件名字
        :param update_callback: 下载更新的回调函数
        :param finished_callback: 下载完成的回调函数
        :param chunk_size: 每次分包下载的大小
        """
        super().__init__()
        self.session = session
        self.url = url
        self.path = path
        self.file_name = file_name
        self.update_callback = update_callback
        self.finished_callback = finished_callback
        self.chunk_size = chunk_size

    def run(self):
        # 创建缓存文件夹
        if not os.path.exists(self.path):
            logging.info("缓存文件夹[%s]不存在!" % self.path)
            os.makedirs(self.path)
            logging.info("创建缓存文件夹[%s]..." % self.path)
        # 对文件名进行MD5加密
        md5 = hashlib.md5()
        md5.update(self.file_name.encode('utf8'))
        file_name = md5.hexdigest()
        file_name = self.path + file_name
        # 查找缓存文件
        if os.path.exists(file_name):
            logging.info("发现缓存文件[%s]" % file_name)
        else:
            with closing(self.session.get(self.url, stream=True)) as response:
                logging.info("开始下载文件:[url:%s, 保存位置:%s]" % (self.url, file_name))
                content_size = int(response.headers['content-length'])  # 文件总大小
                s = 0
                with open(file_name, 'wb') as file:
                    for data in response.iter_content(chunk_size=self.chunk_size):
                        file.write(data)
                        s += len(data)
                        # 回调下载进度函数
                        if callable(self.update_callback):
                            self.update_callback(s / content_size)
                logging.info('文件下载完成[%s].' % file_name)
        # 回调下载完成函数
        if callable(self.finished_callback):
            self.finished_callback(file_name)

    @staticmethod
    def parse(core, use_qq):
        if use_qq:
            session = core.qq.session
        else:
            session = core.netease.session
        return session

    @staticmethod
    def download_mp3(core, use_qq, song, file, update_callback, finished_callback):
        """ 下载MP3音乐文件,参数参见 DownloadThread 构造函数 """
        path = config.cache_path + 'mp3/'
        session = DownloadThread.parse(core, use_qq)
        url = core.song_url(song, use_qq)
        DownloadThread.download(session, url, path, file, update_callback, finished_callback)

    @staticmethod
    def download_img(core, use_qq, song, file, update_callback, finished_callback):
        """ 下载图片文件,参数参见 DownloadThread 构造函数 """
        path = config.cache_path + 'img/'
        session = DownloadThread.parse(core, use_qq)
        url = core.album_img_url(song, use_qq)
        DownloadThread.download(session, url, path, file, update_callback, finished_callback)

    @staticmethod
    def download(session, url, path, file, update_callback, finished_callback):
        """ 下载文件,参数参见 DownloadThread 构造函数 """
        thread = DownloadThread(session, url, path, file, update_callback, finished_callback)
        thread.start()


download_mp3 = DownloadThread.download_mp3
download_img = DownloadThread.download_img


class SONG(QSong, NSong):
    @staticmethod
    def merger_song(qsong, nsong):
        """
        将两个音乐信息合并
        :param qsong: qq音乐
        :param nsong: 网易云音乐
        :return: 合并结果
        """
        song = SONG()
        song.qid = qsong.id
        song.mid = qsong.mid
        song.nid = nsong.id
        song.name = qsong.name
        album = ALBUM()
        album.mid = qsong.album.mid
        album.name = qsong.album.name
        album.pic_url = nsong.album.pic_url
        song.album = album
        song.action = qsong.action
        song.pay = qsong.pay
        song.dt = qsong.dt
        song.url = nsong.url
        song.artists = qsong.artists
        song.f = QQ | NETEASE
        return song

    @staticmethod
    def merger_album(qalbum, nalbum):
        album = Album()
        album

    def __init__(self):
        super(QSong, self).__init__()
        super(NSong, self).__init__()
        self.f = 0
        self.qid = 0
        self.nid = 0

class ALBUM(QAlbum,NAlbum):
    def __init__(self):
        pass
