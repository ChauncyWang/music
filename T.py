import logging
import os
import sys

from PyQt5.QtWidgets import QApplication

from ui.components import MainWindow
from ui import resource
from util import load_config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(filename)s:%(lineno)d) [%(threadName)s]-[%(levelname)s]: %(message)s',)

app = QApplication(sys.argv)
# a = Crawler()
# play = PlayBar()
# play.show()
# play.set_song(a.search_songs("告白气球", 0, 1)[0])
a = MainWindow()
load_config()
a.show()
qss = open(os.path.dirname(__file__) + "/ui/Default.qss", 'r').read()
app.setStyleSheet(qss)
sys.exit(app.exec_())
