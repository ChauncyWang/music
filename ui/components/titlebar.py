from PyQt5.QtWidgets import *

from ui.components.base_component import *


class TitleBar(QFrame):
    """
    标题栏
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_icon = AwesomeLabel(self, "search_icon", '\uf002', 30)
        self.input = QLineEdit(self)
        self.min_icon = AwesomeLabel(self, "minimum", '\uf078', 20)
        self.max_icon = AwesomeLabel(self, "maximum", '\uf077', 20)
        self.close_icon = AwesomeLabel(self, "close_icon", '\uf00d', 20)
        self.mouse_press_pos = None
        self.init()
        self.signal_slot()

    def init(self):
        self.input.setGeometry(20, 5, 150, 30)
        self.input.setStyleSheet("color:#FFFFFF;border:2px solid;border-radius:15px;"
                                 "background-color:#80808080;padding-left:10px;")
        self.search_icon.setGeometry(180, 5, 30, 30)
        self.search_icon.setStyleSheet("color:#FFFFFF")

    def paintEvent(self, event):
        self.min_icon.setGeometry(self.width() - 90, 10, 30, 20)
        self.max_icon.setGeometry(self.width() - 60, 10, 30, 20)
        self.close_icon.setGeometry(self.width() - 30, 10, 30, 20)

    def signal_slot(self):
        self.close_icon.clicked.connect(QApplication.exit)

    def mousePressEvent(self, event):
        self.mouse_press_pos = event.pos()

    def mouseMoveEvent(self, event):
        x = event.pos().x() - self.mouse_press_pos.x() + self.parent().pos().x()
        y = event.pos().y() - self.mouse_press_pos.y() + self.parent().pos().y()
        self.parent().setGeometry(x, y, self.parent().width(), self.parent().height())
