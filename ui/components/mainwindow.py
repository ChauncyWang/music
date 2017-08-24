from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QScrollArea

from core import music_core
from task_thread import task
from ui.components.playbar import PlayBar
from ui.components.songlist import SongListBar
from ui.components.songtable import SongTable
from ui.components.titlebar import TitleBar


class MainWindow(QMainWindow):
    """
    主窗口
    """

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.music = music_core
        self.search_task = None

        self.play_bar = PlayBar(self)
        self.title = TitleBar(self)
        self.left_frame = SongListBar(self)
        self.main_frame = SongTable(self)
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

    """def search_song(self):
        text = self.title.input.text()
        if text != "":
            songs = self.music.search(text, 0, 20)
            self.main_frame.songs = songs
    """

    def search_song(self):
        text = self.title.input.text()
        if text != "" and self.search_task is None:
            self.search_task = task(self.music.search, text, 0, 20)
            self.search_task.finish.connect(self.search_result)
            self.search_task.start()

    def search_result(self, songs):
        self.main_frame.songs = songs
        self.search_task = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.search_song()


