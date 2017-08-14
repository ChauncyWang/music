from exception_handle import exception, QParseException
from models import *
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


class Parse:
    @staticmethod
    @exception
    def parse_song(dic):
        try:
            song = QSong()
            song.id = dic['id']
            song.mid = dic['mid']
            song.name = dic['name']
            song.artists = Parse.parse_artists(dic['singer'])
            song.album = Parse.parse_album(dic['album'])
            song.dt = dic['interval'] * 1000
            song.action = dic['action']['msg']
            song.pay = dic['pay']['pay_down']
            return song
        except KeyError:
            raise QParseException("Parse Song Exception")

    @staticmethod
    @exception
    def parse_artist(dic):
        try:
            artist = QArtist()
            artist.id = dic['id']
            artist.mid = dic['mid']
            artist.name = dic['name']
            return artist
        except KeyError:
            raise QParseException("Parse Artist Exception")

    @staticmethod
    def parse_artists(dic):
        artists = Artists()
        for i in dic:
            artist = Parse.parse_artist(i)
            artists.append(artist)
        return artists

    @staticmethod
    @exception
    def parse_album(dic):
        try:
            album = QAlbum()
            album.id = dic['id']
            album.mid = dic['mid']
            album.name = dic['name']
            return album
        except KeyError:
            raise QParseException("Parse Album Exception")
