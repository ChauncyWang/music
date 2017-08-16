from PyQt5.QtWidgets import QLineEdit

from ui import awesome
from ui.components.base_component import *


class SongListsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = ClickableLabel(self)
        self.icon_add = ClickableLabel(self)
        self.icon_fold = ClickableLabel(self)
        self.frame_items = SongListsFrame.ListFrame(self)
        self.edit_name = QLineEdit(self)
        self.folded = True
        self.init_components()
        self.signal_slot()

    def init_components(self):
        label_qss = """
            QLabel{font: %dpx;color:#AAAAAA;}QLabel:hover{color:#FFFFFF;}
        """
        self.icon_add.setStyleSheet(label_qss % 12)
        self.icon_add.setText('\uE083')
        self.icon_add.setAlignment(Qt.AlignCenter)
        self.icon_fold.setStyleSheet(label_qss % 14)
        self.title.setStyleSheet(label_qss % 10)
        self.title.setGeometry(10, 0, 100, 25)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(label_qss % 14)
        self.title.setText("我创建的歌单")
        self.edit_name.setGeometry(10, 27, 100, 21)
        self.edit_name.hide()
        self.frame_items.setGeometry(0, 25, 0, 0)

    def signal_slot(self):
        self.title.clicked.connect(self.folded_update)
        self.icon_fold.clicked.connect(self.folded_update)
        self.icon_add.clicked.connect(self.add_item)

    def folded_update(self):
        """ 更新折叠状态 """
        self.folded = not self.folded
        self.update()

    def add_item(self):
        self.folded = False
        self.edit_name.show()
        self.edit_name.setFocus()
        self.frame_items.setGeometry(0, 50, self.frame_items.width(), self.frame_items.height())
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            text = self.edit_name.text()
            if text == "" or text is None:
                text = "未命名歌单"

            self.frame_items.add_item(text)
            self.frame_items.setGeometry(0, 25, self.frame_items.width(), self.frame_items.height())
            self.edit_name.hide()
            self.update()

    def paintEvent(self, event):
        w = self.width()
        self.icon_add.setGeometry(w - 50, 0, 25, 25)
        self.icon_fold.setGeometry(w - 25, 0, 25, 25)
        if not self.folded:
            self.icon_fold.setText(awesome.icon_angle_up)
            self.setFixedSize(160, self.frame_items.height() + self.frame_items.pos().y())
        else:
            self.icon_fold.setText(awesome.icon_angle_down)
            self.setFixedSize(160, 25)

    class ItemFrame(QFrame):
        """ 列表项 """

        def __init__(self, parent=None, text="未命名歌单", icon=awesome.icon_music):
            super().__init__(parent)
            self.setStyleSheet("ItemFrame:hover{background-color:#40FFFFFF;margin: 2px 10px 2px 4px;padding-left:10px;}"
                               "ItemFrame {margin: 2px 10px 2px 4px;padding-left:10px;}")
            self.setFixedSize(160, 25)
            self.icon = QLabel(self)
            self.icon.setStyleSheet("font: 14px 'FontAwesome';color:#FFFFFF;")
            self.icon.setAlignment(Qt.AlignCenter)
            self.icon.setGeometry(20, 0, 25, 25)
            self.icon.setText(icon)
            self.label = QLabel(self)
            self.label.setStyleSheet('font: 12px;color:#FFFFFF')
            self.label.setAlignment(Qt.AlignVCenter)
            self.label.setGeometry(50, 0, 110, 25)
            self.label.setText(text)

    class ListFrame(QFrame):
        """ 列表项(点击箭头显示出来的部分) """

        def __init__(self, parent):
            super().__init__(parent)
            self.items = []

        def add_item(self, item, icon=awesome.icon_music):
            """ 添加列表项目 """
            frame = SongListsFrame.ItemFrame(self, icon)
            frame.label.setText(item)
            frame.show()
            self.items.insert(0, frame)
            for i in range(0, len(self.items)):
                self.items[i].setGeometry(0, i * 25, 160, 25)
            self.setFixedSize(160, 25 * len(self.items))
            self.update()


class SongListBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.likes = SongListsFrame.ItemFrame(self, "我喜欢", awesome.icon_heart)
        self.history = SongListsFrame.ItemFrame(self, "播放历史", awesome.icon_time)
        self.lists = SongListsFrame(self)
        self.likes.setGeometry(0, 200, 160, 25)
        self.history.setGeometry(0, 225, 160, 25)
        self.lists.setGeometry(0, 250, 160, 25)

    def paintEvent(self, event):
        self.setFixedSize(160, self.lists.height() + self.lists.pos().y())
