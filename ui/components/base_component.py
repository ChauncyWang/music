import threading

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainterPath, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui.config import *


class ClickableLabel(QLabel):
    """
    拥有点击事件信号的 QLabel,
    在 mousePressEvent 中发射信号
    """
    clicked = pyqtSignal()

    def __init__(self, parent=None, text=None):
        super(QLabel, self).__init__(parent, text=text)
        self.enter = False
        self.padding = 0
        self.timer = None
        self.inc = 1
        self.show_text = None

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, *args, **kwargs):
        self.show_text = self.text()
        text_width = self.fontMetrics().width(self.show_text)
        d_width = text_width - self.width()
        if d_width > 0:
            self.padding = 0
            self.timer = threading.Timer(0.2, self.update_loc, args={d_width})
            self.timer.start()

    def leaveEvent(self, *args, **kwargs):
        if self.timer is not None:
            self.timer.cancel()
            self.setText(self.show_text)

    def update_loc(self, d_width):
        self.padding += 1
        if self.padding == len(self.show_text):
            self.padding = 0
        self.setText(self.show_text[self.padding:])
        self.update()
        self.timer = threading.Timer(0.2, self.update_loc, args={d_width})
        self.timer.start()


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


class FoldList(QFrame):
    """ 可折叠列表 """
    folded_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.folded = True
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)
        self.childrens = None

    def fold(self):
        """ 修改折叠状态 """
        self.folded = not self.folded
        if self.folded:
            for item in self.childrens:
                self.layout().removeWidget(item)
        else:
            for item in self.childrens:
                self.layout().addWidget(item)
        self.folded_changed.emit(self.folded)


class IconLabel(ClickableLabel):
    qq = "url(:/png/qqmusic)"
    netease = "url(:/png/netease)"

    def __init__(self, parent, icon, text):
        super().__init__(parent, text)
        self.icon = icon
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border-image:%s;color:#00000000;" % self.icon)

    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet("border-image:none;font: 20px 'FontAwesome'; color:#%s;" % theme_color)

    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet("border-image:%s;color:#00000000;" % self.icon)
