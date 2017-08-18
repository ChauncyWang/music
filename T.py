import logging
import os
import sys

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from ui import resource
from ui.components.mainwindow import MainWindow
try:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s (%(filename)s:%(lineno)d) [%(threadName)s]-[%(levelname)s]: %(message)s',)

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # a = Crawler()
    # play = PlayBar()
    # play.show()
    # play.set_song(a.search_songs("告白气球", 0, 1)[0])

    font_file = os.path.dirname(__file__) + '/ui/res/font/fontawesome-webfont.ttf'
    if QFontDatabase.addApplicationFont(font_file) == -1:
        logging.warning("字体加载失败,有部分图标将无法显示!")
    else:
        logging.info("字体文件加载成功!")

    main = MainWindow()
    qss = open(os.path.dirname(__file__) + "/ui/Default.qss", 'r').read()
    app.setStyleSheet(qss)
    main.show()
    sys.exit(app.exec_())
except BaseException as e:
    e.with_traceback()
