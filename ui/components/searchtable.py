from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from models import Song
from ui.components.base_component import FromFrame


class SearchTable(QTableWidget):
    play_song = pyqtSignal(Song, bool)

    def __init__(self, core, parent=None):
        super(QTableWidget, self).__init__(parent)
        self.songs = []
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.music = core
        self.setStyleSheet("""
            QScrollBar {
                background:write;
            }
            QScrollBar::handle {
                background:lightgray;
                border:2px solid red;
                border-radius:5px;
            }
            QScrollBar::handle:hover {
                background:gray;
            }
            QScrollBar::sub-line {
                background:transparent;
            }
            QScrollBar::add-line {
                background:transparent;
            }""")
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def set_songs(self, songs):
        self.songs = songs
        self.update_model()

    def update_model(self):
        self.clear()
        self.setColumnCount(4)
        self.setRowCount(1 + len(self.songs))
        self.setHorizontalHeaderItem(0, QTableWidgetItem("歌曲"))
        self.setHorizontalHeaderItem(1, QTableWidgetItem("歌手"))
        self.setHorizontalHeaderItem(2, QTableWidgetItem("专辑"))
        self.setHorizontalHeaderItem(3, QTableWidgetItem("歌曲来源"))
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        for i in range(0, len(self.songs)):
            self.setItem(i, 0, QTableWidgetItem(self.songs[i - 1].name))
            self.setItem(i, 1, QTableWidgetItem(str(self.songs[i - 1].artists)))
            self.setItem(i, 2, QTableWidgetItem(self.songs[i - 1].album.name))
            f = self.music.playable(self.songs[i - 1])
            lab = FromFrame(self, f, self.songs[i - 1])
            lab.signal_play.connect(self.play_clicked)
            self.setCellWidget(i, 3, lab)

    def play_clicked(self, song, use_qq):
        """ 某个播放键点击了 """
        self.play_song.emit(song, use_qq)


