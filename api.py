from abc import ABCMeta, abstractmethod


class BaseAPI(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url, params=None, headers=None, stream=False):
        """ get请求 """
        pass

    @abstractmethod
    def post(self, url, data=None, headers=None):
        """ post请求 """
        pass

    @abstractmethod
    def search(self, content, t, page, num):
        """
        搜索
        :param content:搜索内容
        :param t:搜索类型
        :param page:页码
        :param num:每页大小
        :return:指定搜索类型的搜索结果
        """
        pass

    @abstractmethod
    def search_songs(self, content, page, num):
        """
        搜索歌曲
        :param content:搜索内容
        :param page:页码
        :param num:每页大小
        :return:搜索到的歌曲
        """
        pass

    @abstractmethod
    def search_artists(self, content, page, num):
        """
        搜索歌手
        :param content:搜索内容
        :param page:页码
        :param num:每页大小
        :return:搜索到的歌手
        """
        pass

    @abstractmethod
    def lyric(self, song):
        """
        获取歌曲歌词的url
        :param song: 要获取歌词的歌曲
        :return: 歌词的url
        """
        pass

    @abstractmethod
    def song_url(self, song):
        """
        获取歌曲的播放地址
        :param song: 要获取播放地址的歌曲
        :return: 歌曲播放地址
        """

    @abstractmethod
    def playable(self, song):
        """
        查看歌曲是否能播放
        :param song: 要判断的歌曲
        """

    @abstractmethod
    def album_img_url(self, song):
        """
        获取专辑头像地址
        :param song: 要获取头像的歌曲
        :return: 歌曲专辑的头像地址
        """