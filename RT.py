import sys

from ui.components import *
from ui import resource
import logging
import requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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

def test_media():
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile('D:\\ChavaMusic\\cache\\mp3\\我们的歌谣True.m4a')))
    player.play()
    print(player.state())
    sys.exit(app.exec_())

test_media()
