import gc
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QFrame, QLabel, QWidget, QVBoxLayout

from models import Song, Songs
from ui.awesome import *
from ui.components.base_component import ClickableLabel
from ui.config import theme_color


class SongTable(QFrame):
    def __init__(self, parent=None):
        self.songs = None
        super().__init__(parent)
        self.setFixedSize(600,30)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.setStyleSheet("SongTable{background-color:#A0000000;}")

    @property
    def songs(self):
        return self._songs

    @songs.setter
    def songs(self, songs):
        if isinstance(songs, Songs):
            self._songs = songs
            self.setFixedSize(self.width(), (len(songs) + 1) * 30)
            layout = self.layout()
            # 删除之前所有控件
            for i in range(0, layout.count()):
                widget = layout.itemAt(0).widget()
                widget.setParent(None)
                layout.removeWidget(widget)
            # 重新生成控件
            for i, song in enumerate(songs):
                item = SongTableItem(song)
                item.setFixedSize(600, 30)
                layout.addWidget(item)
            self.update()



class SongTableHeader(QFrame):
    pass


class SongTableItem(QFrame):
    def __init__(self, song,parent=None):
        super().__init__(parent)
        self.cl_name = ClickableLabel(self)
        self.cl_artist = ClickableLabel(self)
        self.cl_album = ClickableLabel(self)
        self.cl_play = ClickableLabel(self, icon_play_circle)
        self.cl_like = ClickableLabel(self, icon_heart_empty)
        self.cl_add = ClickableLabel(self, icon_plus_sign)
        self.l_time = QLabel(self)
        self.init_components()
        self.song = song

    def init_components(self):
        self.setStyleSheet('SongTableItem {;} SongTableItem:hover{background-color:#20FFFFFF;}'
                           'ClickableLabel{%s}ClickableLabel:hover{%s} QLabel{color:#80FFFFFF;}'
                           % (awesome_qss % (14,"80FFFFFF"), awesome_qss % (14,theme_color)))
        self.cl_play.hide()
        self.cl_like.hide()
        self.cl_add.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(0xff, 0xff, 0xff, 0x80))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(10, 0, self.width() - 10, 0)

        w = (self.width() - 20) // 10
        h = self.height()
        m = self.cl_name.fontMetrics()
        self.cl_name.setGeometry(10, 0, m.width(self.cl_name.text()), h)
        self.cl_artist.setGeometry(w * 5, 0, w * 2, h)
        self.cl_album.setGeometry(w * 7, 0, w * 2, h)
        self.l_time.setGeometry(w * 9, 0, w, h)

    def enterEvent(self, *args, **kwargs):
        w = (self.width() - 20) / 2
        h = self.height()
        self.cl_play.setGeometry(w - h * 3, 0, h, h)
        self.cl_play.show()
        self.cl_like.setGeometry(w - h * 2, 0, h, h)
        self.cl_like.show()
        self.cl_add.setGeometry(w - h, 0, h, h)
        self.cl_add.show()

    def leaveEvent(self, *args, **kwargs):
        self.cl_play.hide()
        self.cl_like.hide()
        self.cl_add.hide()

    @property
    def song(self):
        return self._song

    @song.setter
    def song(self, song):
        if isinstance(song, Song):
            self.cl_name.setText(song.name)
            self.cl_artist.setText(str(song.artists))
            self.cl_album.setText(str(song.album))
            self.l_time.setText("%02d:%02d" % (song.dt // 1000 // 60, song.dt // 1000 % 60))
        self.update()
