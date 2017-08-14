from models import Song, Album, Artist, Quality, Artists, Songs
from exception_handle import exception, NParseException
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

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.alias = None
        self.img_url = None


class NArtists(Artists):
    def __init__(self, dic):
        super().__init__()
        if dic is not None:
            for t in dic:
                self.append(Parse.parse_artist(t))


class NAlbum(Album):
    """
    网易专辑
    """

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.type = None
        self.size = None
        self.pic_url = None
        self.artists = None


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
        """
        解析歌曲
        :param dic:包含歌曲信息的 json 数据
        :return: 解析结果
        """
        try:
            song = NSong()
            song.id = dic.get('id')
            song.name = dic.get('name')
            song.artists = NArtists(dict_adapter(dic, 'ar', 'artist', 'artists'))
            alias = dic.get('alia')
            alias1 = dic.get('alias')
            song.alias = alias1 if alias is None else alias
            song.album = Parse.parse_album(dict_adapter(dic, 'al', 'album', 'albums'))
            song.mv = dic.get('mv')
            song.dt = dict_adapter(dic, 'dt', 'duration')
            return song
        except KeyError:
            raise NParseException('Parse song exception!')

    @staticmethod
    @exception
    def parse_artist(dic):
        """
        解析歌手信息
        :param dic:包含歌手信息的 json 数据
        :return: 解析出的歌手信息
        """
        try:
            artist = NArtist()
            artist.id = dic.get('id')
            artist.name = dic.get('name')
            artist.alias = dic.get('alias')
            artist.img_url = dic.get('img1v1Url')
            return artist
        except KeyError:
            raise NParseException('Parse song exception!')

    @staticmethod
    @exception
    def parse_album(dic):
        """
        解析专辑信息
        :param dic: 包含专辑信息的 json 数据
        :return: 解析的专辑信息
        """
        try:
            album = NAlbum()
            album.id = dic.get('id')
            album.name = dic.get('name')
            album.type = dic.get('type')
            album.size = dic.get('size')
            album.pic_url = dic.get('picUrl')
            album.artists = NArtists(dic.get('artists'))
            return album
        except KeyError:
            raise NParseException('Parse song exception!')
