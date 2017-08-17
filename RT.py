
import logging
import os
import sys

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow

from models import Song
from ui import resource
from ui.components.mainwindow import MainWindow
from ui.components.songtable import SongTableItem

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(filename)s:%(lineno)d) [%(threadName)s]-[%(levelname)s]: %(message)s',)

QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
font_file = os.path.dirname(__file__) + '/ui/res/font/fontawesome-webfont.ttf'
if QFontDatabase.addApplicationFont(font_file) == -1:
    logging.warning("字体加载失败,有部分图标将无法显示!")
else:
    logging.info("字体文件加载成功!")
main = QMainWindow()
main.setStyleSheet("QMainWindow{background-color:#660099;}")
song = Song()
song.name = "gaobaiqiqiu"
song.artists = "人"
song.album = "专辑"
song.dt = 2000000
a = SongTableItem(main, song)
main.show()
sys.exit(app.exec_())
