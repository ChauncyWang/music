from PyQt5.QtWidgets import QFrame

from ui.components.base_component import ClickableLabel


class SongTable(QFrame):
    pass


class SongTableHeader(QFrame):
    pass


class SongTableItem(QFrame):
    def __init__(self, parent, song=None):
        super().__init__(parent)
        self.song = song
        self.cl_name = ClickableLabel(self)
