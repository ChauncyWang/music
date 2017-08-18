import logging
from random import Random


class Song:
    """
    歌曲
    """

    def __init__(self):
        self.name = None
        self.artists = None
        self.album = None
        self.dt = 0
        self.f = 0

    def __str__(self):
        m = self.dt // 1000 // 60
        s = self.dt // 1000 % 60
        return "[(歌曲:%s)(歌手:%s)(专辑:%s)(时间:%02d:%02d)]" % (self.name, self.artists, self.album, m, s)

    def __eq__(self, other):
        if isinstance(other, Song):
            a = self.name == other.name
            b = self.album.name == other.album.name
            c = self.artists == other.artists
            return a and b and c


class Songs(list):
    def __str__(self):
        s = ''
        for t in self:
            if isinstance(t, Song):
                s += t.name
                s += '/'
        return s[:len(s) - 1]


class Artist:
    """
    艺术家，演唱者，歌手
    """

    def __init__(self):
        self.name = None

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class Artists(list):
    def __init__(self):
        super().__init__()

    def __str__(self):
        s = ''
        for t in self:
            if isinstance(t, Artist):
                s += t.name
                s += '/'

        s = s[:len(s) - 1]
        return s


class Album:
    """
    专辑
    """

    def __init__(self):
        self.name = None
        self.artists = None

    def __str__(self):
        return '%s' % self.name


class Quality:
    def __init__(self):
        self.bit_rate = None
        self.size = None


class SongList:
    """
    播放列表
    """
    # 列表循环
    ListLoop = 1
    # 单曲循环
    SingleLoop = 2
    # 随机循环
    RandomLoop = 3

    def __init__(self, name):
        self.songs = []
        self.name = name
        self.mode = SongList.ListLoop
        self.index = 0

    def add(self, song):
        """
        向列表添加
        :param song:
        :return:
        """
        if isinstance(song, Song):
            self.songs.append(song)
            logging.debug("添加[%s]到列表[%s]" % (str(song), self.name))
        else:
            logging.warning("你在歌曲列表[%s]添加了什么？[%s]" % (self.name, str(song)))

    def remove(self, song):
        """
        从列表中删除
        :param song:要删除的歌曲
        """
        if isinstance(song, Song):
            if self.index >= self.songs.index(song):
                self.index -= 1

            self.songs.remove(song)
            logging.debug("从列表[%s]中删除[%s]" % (self.name, str(song)))
        else:
            logging.warning("你想从歌曲列表[%s]删除什么？[%s]" % (self.name, str(song)))

    def pre(self):
        pass

    def next(self):
        """ 下一曲 """
        if self.mode == SongList.ListLoop:
            self.index += 1
            if self.index >= len(self.songs):
                self.index = 0
        elif self.mode == SongList.SingleLoop:
            pass
        elif self.mode == SongList.RandomLoop:
            self.index = Random().randint(0, len(self.songs) - 1)

        return self.songs[self.index]
