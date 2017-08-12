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
        s = self.dt // 1000 - 60 * m
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
        return '%s,%s' % (self.name, str(self.artists))


class Quality:
    def __init__(self):
        self.bit_rate = None
        self.size = None
