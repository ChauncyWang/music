import re
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QColor, QPen
from PyQt5.QtWidgets import *

from util import Configuration


class Lyric(QFrame):
    def __init__(self, parent=None):
        super(QFrame, self).__init__(parent)
        self.lyric = QLabel(self)
        self.lyric2 = QLabel(self)
        self.single_line = True
        self.lock = False
        self.enter = False
        self.press = False
        self.press_x = 0
        self.press_y = 0

        self.lyrics = None
        self.init()

    def init(self):
        Configuration.load_config()
        configuration = Configuration.config
        x = Configuration.get(100, 'ui', 'lyric', 'x')
        y = Configuration.get(800, 'ui', 'lyric', 'y')
        w = Configuration.get(400, 'ui', 'lyric', 'w')
        h = Configuration.get(80, 'ui', 'lyric', 'h')
        self.single_line = Configuration.get(False, 'ui', 'lyric', 'single')
        self.setGeometry(x, y, w, h)
        self.setObjectName('lyric_bar')
        self.setWindowFlags(Qt.SubWindow | Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.lyric.setObjectName('lyric')
        self.lyric2.setObjectName('lyric2')
        self.lyric2.hide()

    def set_lyrics(self, lyric):
        self.lyrics = lyric.split('\n')

    def update_lyric(self, x):
        lyric_index = 0
        while lyric_index < len(self.lyrics) - 1:
            line = self.lyrics[lyric_index]
            result = re.search(r'\[(\d*):(\d*).(\d*)]', line)
            if result is None:
                lyric_index += 1
            else:
                time = int(result.group(1)) * 1000 * 60 + int(result.group(2)) * 1000 + int(result.group(3))
                if time <= x + 0.2:
                    line = line[line.index(']') + 1:]
                    line2 = self.lyrics[lyric_index + 1]
                    line2 = line2[line2.index(']') + 1:]
                    if not self.single_line:
                        if lyric_index % 2 == 0:
                            self.lyric.setText(line)
                            self.lyric.setStyleSheet('color: #00FF80;')
                            self.lyric2.setText(line2)
                            self.lyric2.setStyleSheet('color: #FF0080;')
                        else:
                            self.lyric2.setText(line)
                            self.lyric2.setStyleSheet('color: #00FF80;')
                            self.lyric.setText(line2)
                            self.lyric.setStyleSheet('color: #FF0080;')

                        self.update()
                    else:
                        self.lyric.setText(line)
                    lyric_index += 1
                else:
                    break

    def paintEvent(self, event):
        p1 = 10
        p2 = 20
        if self.single_line:
            self.lyric.setGeometry(p1, p2, self.width() - 2 * p1, self.height() - p1 - p2)
            self.lyric.setAlignment(Qt.AlignCenter)
            self.lyric2.hide()
        else:
            w = self.width() - 2 * p1
            h = (self.height() - p1 - p2) / 2
            self.lyric.setGeometry(p1, p2, w, h)
            self.lyric.setAlignment(Qt.AlignLeft)
            self.lyric2.setGeometry(p1, p2 + h, w, h)
            self.lyric2.setAlignment(Qt.AlignRight)
            self.lyric2.show()
        font = QFont()
        font.setPixelSize(self.lyric.height() * 0.8)
        self.lyric.setFont(font)
        self.lyric2.setFont(font)

        if not self.lock:
            if self.enter:
                self.setCursor(Qt.OpenHandCursor)
                painter = QPainter(self)
                path = QPainterPath()
                rect = QRectF(0, 0, self.width(), self.height())
                path.addRoundedRect(rect, 10, 10)
                painter.fillPath(path, QColor(0, 0, 0, 55))
                pen = QPen()
                pen.setWidth(2)
                pen.setColor(QColor(255, 255, 255, 180))
                painter.setPen(pen)
                painter.drawRoundedRect(self.rect(), 10, 10)
                painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, 8, 8)

        Configuration.config['ui']['lyric']['x'] = self.pos().x()
        Configuration.config['ui']['lyric']['y'] = self.pos().y()
        Configuration.config['ui']['lyric']['w'] = self.width()
        Configuration.config['ui']['lyric']['h'] = self.height()
        Configuration.config['ui']['lyric']['single'] = self.single_line
        Configuration.save_config()

    def enterEvent(self, event):
        self.enter = True
        self.update()

    def leaveEvent(self, event):
        self.enter = False
        self.update()

    def resizeEvent(self, event):
        self.enter = True

    def mousePressEvent(self, event):
        self.press = True
        self.press_x = event.pos().x()
        self.press_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.press = False

    def mouseMoveEvent(self, event):
        if self.press:
            dx = self.pos().x() + event.pos().x() - self.press_x
            dy = self.pos().y() + event.pos().y() - self.press_y
            self.setGeometry(dx, dy, self.width(), self.height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.single_line = not self.single_line
        self.update()


