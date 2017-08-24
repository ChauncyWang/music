import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QFrame, QLabel, QWidget, QVBoxLayout, QScrollArea

from api.netease import NETEASE
from api.qq import QQ
from core import music_core
from models import Song, Songs
from ui.awesome import *
from ui.components.base_component import ClickableLabel, IconLabel
from ui.config import theme_color


class SongTable(QFrame):
    """ 歌曲列表 """
    play_song = pyqtSignal(Song, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.songs = None
        self.scroll = QScrollArea(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget = QWidget(self)
        self.widget.setLayout(layout)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""QScrollArea{background-color:#A0000000;}
            QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar:up-arrow:vertical, QScrollBar:down-arrow:vertical { background: #00000000;}
            QScrollBar:vertical { background: #20FFFFFF;width:8px;}
            QScrollBar::handle:vertical { border-radius:4px;width:8px;background: #40FFFFFF;}
        """)
        self.widget.setStyleSheet("background-color:#00000000;")
        self.scroll.setWidget(self.widget)

    def paintEvent(self, event):
        self.scroll.setGeometry(0, 0, self.width(), self.height())

    @property
    def songs(self):
        return self._songs

    @songs.setter
    def songs(self, songs):
        if isinstance(songs, Songs):
            self._songs = songs
            self.widget.setFixedSize(self.width(), (len(songs) + 1) * 30)
            layout = self.widget.layout()
            # 删除之前所有控件
            for i in range(0, layout.count()):
                widget = layout.itemAt(0).widget()
                widget.signal_play.disconnect(self.play_clicked)
                widget.setParent(None)
                layout.removeWidget(widget)
            # 重新生成控件
            for i, song in enumerate(songs):
                item = SongTableItem(song)
                item.setFixedSize(600, 30)
                layout.addWidget(item)
                item.signal_play.connect(self.play_clicked)
            self.update()

    def play_clicked(self, song, use_qq):
        """ 某个播放键点击了 """
        logging.info("[播放]%s -> %s" % ("QQ音乐" if use_qq else "网易云音乐", str(song)))
        self.play_song.emit(song, use_qq)


class SongTableHeader(QFrame):
    pass


class SongTableItem(QFrame):
    signal_play = pyqtSignal(Song, bool)

    def __init__(self, song, parent=None):
        super().__init__(parent)
        self.cl_name = ClickableLabel(self)
        self.cl_artist = ClickableLabel(self)
        self.cl_album = ClickableLabel(self)
        self.cl_play_qq = IconLabel(self, IconLabel.qq, icon_play_circle)
        self.cl_play_netease = IconLabel(self, IconLabel.netease, icon_play_circle)
        self.cl_like = ClickableLabel(self, icon_heart_empty)
        self.cl_add = ClickableLabel(self, icon_plus_sign)
        self.l_time = QLabel(self)
        self.playable = None
        self.init_components()
        self.signal_slot()
        self.song = song

    def signal_slot(self):
        """ 连接信号和槽 """
        # 使用 qq音乐的源播放音乐
        self.cl_play_qq.clicked.connect(lambda: self.signal_play.emit(self.song, True))
        # 使用 网易云音乐的源播放音乐
        self.cl_play_netease.clicked.connect(lambda: self.signal_play.emit(self.song, False))

    def init_components(self):
        self.setStyleSheet('SongTableItem {;} SongTableItem:hover{background-color:#20FFFFFF;}'
                           'ClickableLabel{%s}ClickableLabel:hover{%s} QLabel{color:#80FFFFFF;}'
                           % (awesome_qss % (14, "80FFFFFF"), awesome_qss % (14, theme_color)))
        self.cl_play_qq.hide()
        self.cl_play_netease.hide()
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
        cl_name_w = m.width(self.cl_name.text())
        self.cl_name.setGeometry(10, 0, cl_name_w if cl_name_w < w * 5 else w * 5, h)
        self.cl_artist.setGeometry(w * 5, 0, w * 2, h)
        self.cl_album.setGeometry(w * 7, 0, w * 2, h)
        self.l_time.setGeometry(w * 9, 0, w, h)

    def enterEvent(self, *args, **kwargs):
        w = (self.width() - 20) / 2
        h = self.height()
        self.cl_play_qq.setGeometry(w - h * 4, (h - 20) / 2, 20, 20)
        if (self.playable & QQ) != 0:
            self.cl_play_qq.show()
        self.cl_play_netease.setGeometry(w - h * 3, (h - 20) / 2, 20, 20)
        if (self.playable & NETEASE) != 0:
            self.cl_play_netease.show()
        self.cl_like.setGeometry(w - h * 2, 0, h, h)
        self.cl_like.show()
        self.cl_add.setGeometry(w - h, 0, h, h)
        self.cl_add.show()

    def leaveEvent(self, *args, **kwargs):
        self.cl_play_qq.hide()
        self.cl_play_netease.hide()
        self.cl_like.hide()
        self.cl_add.hide()

    @property
    def song(self):
        return self._song

    @song.setter
    def song(self, song):
        self._song = song
        if isinstance(song, Song):
            self.cl_name.setText(song.name)
            self.cl_artist.setText(str(song.artists))
            self.cl_album.setText(str(song.album))
            self.l_time.setText("%02d:%02d" % (song.dt // 1000 // 60, song.dt // 1000 % 60))
            self.playable = music_core.playable(song)
        self.update()
