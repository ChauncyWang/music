from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter
from PyQt5.QtWidgets import QWidget, QLabel


class ProcessBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.total_time = 100000
        self.position_time = 0
        self.X = 0

        self.setStyleSheet("background-color: black;")
        pal = QPalette()
        pal.setColor(QPalette.WindowText, QColor(255, 255, 255))
        font = QFont("Courier", 10)
        self.leftLabel = QLabel(self)
        self.rightLabel = QLabel(self)
        self.leftLabel.setAlignment(Qt.AlignCenter)
        self.rightLabel.setAlignment(Qt.AlignCenter)
        self.leftLabel.setGeometry(0, 10, 50, 50)
        self.rightLabel.setGeometry(640, 10, 50, 50)
        self.leftLabel.setFont(font)
        self.rightLabel.setFont(font)
        self.leftLabel.setPalette(pal)
        self.rightLabel.setPalette(pal)
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.start()
        timer.timeout.connect(self.update_pos)

    def update_pos(self):
        self.position_time += 1000
        a = self.position_time / self.total_time
        self.X = a * 580 + 56
        second = self.total_time // 1000
        min = second // 60
        second = second - min * 60
        second2 = self.position_time // 1000
        min2 = second2 // 60
        second2 = second2 - min2 * 60
        t = "%d:%d" % (min, second)
        s = "%d:%d" % (min2, second2)
        print("%d-%d" % (self.position_time, self.total_time))
        self.rightLabel.setText(t)
        self.leftLabel.setText(s)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing)
        base_color = QColor(0, 20, 20)
        in_color = QColor(255, 0, 0)
        out_color = QColor(255, 255, 255)
        painter.setBrush(base_color)
        rect = QRect(55, 32, 580, 6)
        painter.drawRoundedRect(rect, 3, 3)
        painter.setBrush(in_color)
        playrect = QRect(55, 32, self.X - 63, 6)
        painter.drawRoundedRect(playrect, 3, 3)
        painter.setBrush(out_color)
        painter.drawEllipse(self.X - 7, 25, 20, 20)
        painter.setBrush(in_color)
        painter.drawEllipse(self.X, 32, 6, 6)
        painter.restore()
