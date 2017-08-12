import sys

from music.ui.components import *
from music.ui import resource

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s (%(filename)s:%(lineno)d) [%(threadName)s]-[%(levelname)s]: %(message)s', )


def test():
    a = NeteaseAPI().search_songs('S.H.E')
    for t in a:
        print(t)


def test1():
    s = NeteaseAPI()
    a = s.get_toplist()
    print(a[0]['toplist'][0]['name'])
    s.get_toplist_songs(a[0]['toplist'][0]['id'])


def test2():
    s = QQMusicAPI()
    a = s.search_song('告白气球', 0, 1)
    for t in a:
        s.get_lyric(t.id, t.mid)


def test_time_label():
    app = QApplication(sys.argv)
    a = FromFrame(f=3)
    a.show()
    sys.exit(app.exec_())


def testcore():
    core = Core()
    a = core.search("薛之谦", 0, 20)
    print(a)


test_time_label()


