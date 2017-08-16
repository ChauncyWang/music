import logging

from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QFrame, QLabel, QSlider

from models import Song
from netease import NETEASE
from qq import QQ
from ui.config import *


class ClickableLabel(QLabel):
    """
    拥有点击事件信号的 QLabel,
    在 mousePressEvent 中发射信号
    """
    clicked = pyqtSignal()
    send = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.send.emit(self.objectName())


class AwesomeLabel(ClickableLabel):
    """
    使用 awesome 图标字体的标签
    """
    font = QFont('fontawesome')

    def __init__(self, parent, obj_name, text, size):
        super(ClickableLabel, self).__init__(parent)
        self.setObjectName(obj_name)
        AwesomeLabel.font.setPixelSize(size)
        self.setFont(AwesomeLabel.font)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)


class PopFrame(QFrame):
    """
    一个可以跟随图标移动的弹窗
    跟随移动需要在要跟随的控件哪里设置（就是自己计算了）
    """

    def __init__(self):
        super().__init__()
        self.padding = 3
        self.arrow_h = 5
        self.w = 2
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        padding = self.padding
        arrow_h = self.arrow_h
        w = self.w
        path = QPainterPath()
        path.moveTo(self.width() / 2, self.height() - padding)
        path.lineTo(self.width() / 2 - arrow_h / 2, self.height() - padding - arrow_h)
        path.lineTo(padding, self.height() - padding - arrow_h)
        path.lineTo(padding, padding)
        path.lineTo(self.width() - padding, padding)
        path.lineTo(self.width() - padding, self.height() - padding - arrow_h)
        path.lineTo(self.width() / 2 + arrow_h / 2, self.height() - padding - arrow_h)
        path.lineTo(self.width() / 2, self.height() - padding)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(QPen(foreground_color, w))
        painter.drawPath(path)
        painter.fillPath(path, QBrush(QColor.fromRgb(100, 100, 100, 127)))


class FromFrame(QFrame):
    """
    播放图标显示
    根据播放源显示不同的图标
    目前只支持qq音乐盒和网易云音乐
    """
    # 播放信号
    signal_play = pyqtSignal(Song, bool)

    def __init__(self, parent=None, f=0, song=None):
        super().__init__(parent)
        self.qqmusic = ClickableLabel(self)
        self.netease = ClickableLabel(self)
        self.f_qq = (f & QQ) != 0
        self.f_netease = (f & NETEASE) != 0
        self.song = song
        self.init_components()
        self.signal_slot()

    def signal_slot(self):
        """ 连接信号和槽 """
        # 使用 qq音乐的源播放音乐
        self.qqmusic.clicked.connect(lambda: self.signal_play.emit(self.song, True))
        # 使用 网易云音乐的源播放音乐
        self.netease.clicked.connect(lambda: self.signal_play.emit(self.song, False))

    def init_components(self):
        self.setMinimumSize(50, 20)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.qqmusic.setStyleSheet("border-image: url(:/png/qqmusic);")
        self.netease.setStyleSheet("border-image: url(:/png/netease);")

    def paintEvent(self, event):
        w = self.width()
        h = self.height() / 2 - 10
        if self.f_qq and self.f_netease:
            self.qqmusic.setGeometry(w / 2 - 21, h, 20, 20)
            self.netease.setGeometry(w / 2 + 1, h, 20, 20)
        elif self.f_qq:
            self.qqmusic.setGeometry(w / 2 - 10, h, 20, 20)
            self.netease.hide()
        elif self.f_netease:
            self.netease.setGeometry(w / 2 - 10, h, 20, 20)
            self.qqmusic.hide()
        else:
            self.netease.hide()
            self.qqmusic.hide()
