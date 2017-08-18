from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QScrollArea

from core import music_core
from ui.components.playbar import PlayBar
from ui.components.searchtable import SearchTable
from ui.components.songlist import SongListBar
from ui.components.titlebar import TitleBar


class MainWindow(QMainWindow):
    """
    主窗口
    """

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.music = music_core

        self.play_bar = PlayBar(self)
        self.title = TitleBar(self)
        self.left_frame = SongListBar(self)
        self.main_frame = SearchTable(self)
        self.main_frame.update_model()
        self.scroll = QScrollArea(self)
        self.init()
        self.signal_slot()

    def init(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(800, 600)
        self.title.setGeometry(160, 0, 640, 40)
        self.title.setObjectName("title_bar")
        self.left_frame.setGeometry(0, 0, 160, 540)
        self.left_frame.setObjectName("left_frame")
        self.main_frame.setGeometry(160, 40, 640, 500)
        self.main_frame.setObjectName("main_frame")
        self.play_bar.setGeometry(0, 540, 800, 60)
        self.play_bar.setObjectName("play_bar")
        self.setObjectName("main_window")
        self.scroll.setGeometry(0, 0, 160, 540)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet('QScrollArea {background-color:#00000000;}')
        self.scroll.setWidget(self.left_frame)

    def signal_slot(self):
        self.title.search_icon.clicked.connect(self.search_song)
        self.main_frame.play_song.connect(self.play_bar.set_song)

    def search_song(self):
        text = self.title.input.text()
        if text != "":
            songs = self.music.search(self.title.input.text(), 0, 20)
            self.main_frame.set_songs(songs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.search_song()


