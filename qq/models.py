from modles import *
from qq import QQ


class SearchType:
    """
    搜索的类型
    """
    song = 0
    album = 8
    lyric = 7
    mv = 12
    types = {song: '歌曲', album: '专辑', mv: 'MV', lyric: '歌词', }

    @staticmethod
    def str(t):
        return SearchType.types[t]


class QSong(Song):
    def __init__(self):
        self.id = None
        self.mid = None
        self.name = None
        self.dt = None
        self.action = None
        self.pay = None
        self.f = QQ

    def __str__(self):
        min = self.dt // 1000 // 60
        sec = self.dt // 1000 - min * 60
        return "%-s %s %s %02d:%02d" % (self.name, self.artists, self.album.name, min, sec)


class QArtist(Artist):
    def __init__(self):
        self.id = None
        self.mid = None
        self.name = None


class QArtists(Artists):
    def __init__(self):
        super().__init__()


class QAlbum(Album):
    def __init__(self):
        self.id = None
        self.mid = None
        self.name = None
