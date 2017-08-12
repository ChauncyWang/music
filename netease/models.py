from modles import Song, Album, Artist, Quality, Artists, Songs
from exception_handle import exception
from netease import NETEASE
from util import dict_adapter


class NSong(Song):
    """
    网易歌曲信息
    """

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.artists = None
        self.alias = None
        self.album = None
        self.mv = None
        self.dt = None
        self.url = None
        self.f = NETEASE

    def __str__(self):
        min = self.dt // 1000 // 60
        sec = self.dt // 1000 - min * 60
        return "%-s %s %s %02d:%02d" % (self.name, self.artists, self.album.name, min, sec)


class NSongs(Songs):
    def __init__(self):
        super().__init__()


class NArtist(Artist):
    """
    网易歌手
    """

    def __init__(self, dic):
        super().__init__()
        self.id = dic.get('id')
        self.name = dic.get('name')
        self.alias = dic.get('alias')
        self.img_url = dic.get('img1v1Url')


class NArtists(Artists):
    def __init__(self, dic):
        super().__init__()
        if dic is not None:
            for t in dic:
                self.append(NArtist(t))


class NAlbum(Album):
    """
    网易专辑
    """

    def __init__(self, dic):
        super().__init__()
        self.id = dic.get('id')
        self.name = dic.get('name')
        self.type = dic.get('type')
        self.size = dic.get('size')
        self.pic_url = dic.get('picUrl')
        self.artists = NArtists(dic.get('artists'))


class NQuality(Quality):
    """
    网易音乐质量
    """

    def __init__(self, dic):
        super().__init__()
        self.bit_rate = dic.get('br')
        self.size = dic.get('size')


class SearchType:
    """
    搜索的类型
    # 歌曲 1
    # 专辑 10
    # 歌手 100
    # 歌单 1000
    # 用户 1002
    # mv 1004
    # 歌词 1006
    # 主播电台 1009
    """
    song = 1
    album = 10
    artist = 100
    song_sheet = 1000
    user = 1002
    mv = 1004
    lyric = 1006
    radio_station = 1009
    types = {song: '歌曲', album: '专辑', artist: '歌手', song_sheet: '歌单', user: '用户', mv: 'MV', lyric: '歌词',
             radio_station: '电台'}

    @staticmethod
    def str(t):
        return SearchType.types[t]


class Parse:
    @staticmethod
    @exception
    def parse_song(dic):
        song = NSong()
        song.id = dic.get('id')
        song.name = dic.get('name')
        song.artists = NArtists(dict_adapter(dic, 'ar', 'artist', 'artists'))
        alias = dic.get('alia')
        alias1 = dic.get('alias')
        song.alias = alias1 if alias is None else alias
        song.album = NAlbum(dict_adapter(dic, 'al', 'album', 'albums'))
        song.mv = dic.get('mv')
        dt = dic.get('dt')
        dt1 = dic.get('duration')
        song.dt = dt1 if dt is None else dt
        return song
