import os
import re

from PyQt5.QtCore import QRect, Qt, pyqtSignal, QUrl, QRectF, QPropertyAnimation
from PyQt5.QtGui import QPainter, QColor, QFontDatabase, QFont, QPixmap, QPalette, QPen, QBrush, QPainterPath, \
    QFontMetrics
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QLabel, QApplication, QLineEdit, QFrame, QMainWindow, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QComboBox, QSlider, QGraphicsDropShadowEffect

from modles import *
from netease.models import *
from ui.config import *
from core import *

"""
QFontDatabase.addApplicationFont(os.path.dirname(__file__) + '/res/font/fontawesome-webfont.ttf')
font = QFont("fontawesome", 10)
"""


class MainWindow(QMainWindow):
    """
    主窗口
    """

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + '/res/font/fontawesome-webfont.ttf')
        self.music = Core()

        self.play_bar = PlayBar(self.music, self)
        self.title = TitleBar(self)
        self.left_frame = QFrame(self)
        self.main_frame = SearchTable(self.music, self)
        self.main_frame.update_model()
        self.init()
        self.signal_slot()

    def init(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(800, 600)
        self.title.setGeometry(200, 0, 600, 40)
        self.title.setObjectName("title_bar")
        self.left_frame.setGeometry(0, 0, 200, 540)
        self.left_frame.setObjectName("left_frame")
        self.main_frame.setGeometry(200, 40, 600, 500)
        self.main_frame.setObjectName("main_frame")
        self.play_bar.setGeometry(0, 540, 800, 60)
        self.play_bar.setObjectName("play_bar")
        self.setObjectName("main_window")

    def signal_slot(self):
        self.title.search_icon.clicked.connect(self.search_song)
        self.main_frame.play_song.connect(self.play_bar.set_song)

    def search_song(self):
        songs = self.music.search(self.title.input.text(), 0, 20)
        self.main_frame.set_songs(songs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.search_song()


class PlayBar(QFrame):
    """
    音乐播放器下边的播放栏
    """

    def __init__(self, core, parent):
        super().__init__(parent)
        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + '/res/font/fontawesome-webfont.ttf')
        self.play_buttons = PlayButtonGroup(self)
        self.process_bar = ProgressGroup(self)
        self.song_info = QLabel(self)
        self.player = QMediaPlayer()
        self.volume = VolumeButton(self)
        self.lyric = Lyric()
        self.quality = QComboBox(self)

        self.music = core
        self.img = QLabel(self)
        self.song = None
        self.init()
        self.signal_slot()

    def paintEvent(self, event):
        self.play_buttons.setGeometry(0, 0, 0, 0)
        self.img.setGeometry(180, 0, 60, 60)
        self.song_info.setGeometry(250, 0, 200, 30)
        self.process_bar.setGeometry(240, 40, self.width() - 480, 0)
        self.quality.setGeometry(self.width() - 240 - 40, 20, 40, 18)
        self.volume.setGeometry(self.width() - 200, 15, 30, 30)

    def init(self):
        """
        对子控件进行相关的初始化
        """
        style = """
            PlayBar {background-color:#FFFFFF;}
            #cur_time,#total_time,#song_info {color:#AFAFAF;}
            #img {border-width:5px;border-style:double; border-color:#FFFFFF;}
        """
        self.img.setObjectName('img')
        self.song_info.setObjectName('song_info')

        self.quality.addItem("ＨＱ")
        self.quality.addItem("ＳＱ")
        self.quality.addItem("标准")
        f = QFont()
        f.setPixelSize(8)
        self.quality.setFont(f)

        self.lyric.show()

        # self.setStyleSheet(style)

    def signal_slot(self):
        """
        进行信号和槽的链接
        """
        self.play_buttons.signal_play.connect(self.play_pause)
        self.player.positionChanged.connect(self.update_position)
        self.process_bar.signal_rate_changed.connect(self.set_position)
        self.volume.signal_volume_changed.connect(self.player.setVolume)

    def set_song(self, song, use_qq):
        """
        设置 PlayBar 要播放的歌曲
        :param song: 歌曲
        """
        if isinstance(song, Song):
            self.player.stop()
            self.process_bar.slot_loaded(False)
            self.song = song
            self.process_bar.slot_total_time(song.dt)
            self.song_info.setText(song.name + "-" + str(song.artists))
            self.song.br = 320000
            self.process_bar.slot_cur_time(0)
            if isinstance(self.song, SONG):
                if use_qq:
                    self.song.id = self.song.qid
                else:
                    self.song.id = self.song.nid
            download_mp3(self.music, use_qq, song, song.name + str(use_qq),
                         self.download_music_update,
                         self.download_music_finished)
            download_img(self.music, use_qq, song, song.album.name + str(use_qq),
                         None,
                         self.download_head_img_finished)
            self.lyric.set_lyrics(self.music.lyric(self.song, use_qq))
            self.update()

    def play_pause(self, playing):
        """
        播放/暂停切换的槽
        """
        self.play_buttons.playing = playing
        if playing:
            self.player.pause()
        else:
            self.player.play()

    def update_position(self, x):
        self.process_bar.slot_cur_time(x)
        self.lyric.update_lyric(x)
        self.update()

    def download_music_update(self, x):
        """
        歌曲下载过程的槽
        :param x: 下载百分比
        """
        self.process_bar.slot_cur_time(x)

    def download_music_finished(self, file_name):
        """
        歌曲下载完成的槽
        :param file_name: 歌曲存储位置
        """
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        self.player.pause()
        self.player.play()
        self.process_bar.slot_loaded(True)

    def download_head_img_finished(self, file_name):
        """
        头像下载完成的槽
        :param file_name: 头像存储位置
        """
        pic = QPixmap()
        pic.loadFromData(open(file_name, 'rb').read())
        self.img.setPixmap(pic)
        self.img.setScaledContents(True)

    def set_position(self, x):
        self.player.setPosition(x * self.song.dt)
        self.player.play()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.play_pause()


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


class SearchTable(QTableWidget):
    play_song = pyqtSignal(Song, bool)

    def __init__(self, core, parent=None):
        super(QTableWidget, self).__init__(parent)
        self.songs = []
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.music = core
        self.setStyleSheet("""
            QScrollBar {
                background:write;
            }
            QScrollBar::handle {
                background:lightgray;
                border:2px solid red;
                border-radius:5px;
            }
            QScrollBar::handle:hover {
                background:gray;
            }
            QScrollBar::sub-line {
                background:transparent;
            }
            QScrollBar::add-line {
                background:transparent;
            }""")
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def set_songs(self, songs):
        self.songs = songs
        self.update_model()

    def update_model(self):
        self.clear()
        self.setColumnCount(4)
        self.setRowCount(1 + len(self.songs))
        self.setHorizontalHeaderItem(0, QTableWidgetItem("歌曲"))
        self.setHorizontalHeaderItem(1, QTableWidgetItem("歌手"))
        self.setHorizontalHeaderItem(2, QTableWidgetItem("专辑"))
        self.setHorizontalHeaderItem(3, QTableWidgetItem("歌曲来源"))
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        for i in range(0, len(self.songs)):
            self.setItem(i, 0, QTableWidgetItem(self.songs[i - 1].name))
            self.setItem(i, 1, QTableWidgetItem(str(self.songs[i - 1].artists)))
            self.setItem(i, 2, QTableWidgetItem(self.songs[i - 1].album.name))
            f = self.music.playable(self.songs[i - 1])
            lab = FromFrame(self, f, self.songs[i - 1])
            lab.signal_play.connect(self.play_clicked)
            self.setCellWidget(i, 3, lab)

    def play_clicked(self, song, use_qq):
        """ 某个播放键点击了 """
        self.play_song.emit(song, use_qq)


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
        self.setGeometry(400, 800, 800, 80)
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
        while lyric_index < len(self.lyrics):
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


class PlayButton(ClickableLabel):
    PLAY = 1
    PAUSE = 2
    PRE = 3
    NEXT = 4
    texts = {PLAY: '\uf04b', PAUSE: '\uf04c', PRE: '\uf048', NEXT: '\uf051', }

    @staticmethod
    def new_label(kind, parent, size):
        if kind == PlayButton.PLAY:
            label = PlayButton(size, parent, size // 20)
        else:
            label = PlayButton(size, parent)
        label.setText(PlayButton.texts[kind])
        return label

    def __init__(self, size, parent=None, offset=0):
        super().__init__(parent)
        style = """
        color:#%s;border: 2px solid #%s;border-radius:%dpx;padding-left:%dpx
        """ % (theme_color, theme_color, size / 2, offset)
        self.size = size
        self.offset = offset
        self.setFixedSize(size, size)
        self.setStyleSheet(style)
        self.setAlignment(Qt.AlignCenter)


class PlayButtonGroup(QFrame):
    """ 播放相关的按钮组 """
    # 播放信号
    signal_play = pyqtSignal(bool)
    # 上一曲信号
    signal_pre = pyqtSignal()
    # 下一曲信号
    signal_next = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        b, s = playbar_playbtns_big, playbar_playbtns_small
        self.cl_play = PlayButton.new_label(PlayButton.PLAY, self, b)
        self.cl_pause = PlayButton.new_label(PlayButton.PAUSE, self, b)
        self.cl_pre = PlayButton.new_label(PlayButton.PRE, self, s)
        self.cl_next = PlayButton.new_label(PlayButton.NEXT, self, s)
        self.playing = False
        self.init_components()
        self.signal_slot()

    def init_components(self):
        """ 初始化组件 """
        self.setFixedSize(playbar_playbtns_w, playbar_h)
        w, h = self.width(), self.height()
        b, s = playbar_playbtns_big, playbar_playbtns_small
        rect1 = QRect((w - b) / 2, (h - b) / 2, b, b)
        rect2 = QRect((w - b) / 2 - s - 5, (h - s) / 2, s, s)
        rect3 = QRect(w / 2 + b / 2 + 5, (h - s) / 2, s, s)
        self.cl_play.setGeometry(rect1)
        self.cl_pause.setGeometry(rect1)
        self.cl_pre.setGeometry(rect2)
        self.cl_next.setGeometry(rect3)

    def signal_slot(self):
        """ 连接信号和槽 """
        self.cl_play.clicked.connect(self.slot_play_pause)
        self.cl_pause.clicked.connect(self.slot_play_pause)
        self.cl_pre.clicked.connect(self.slot_pre)
        self.cl_next.clicked.connect(self.slot_next)

    def paintEvent(self, event):
        """ 重绘 """
        # 根据播放状态选择显示的控件
        if self.playing:
            self.cl_play.show()
            self.cl_pause.hide()
        else:
            self.cl_pause.show()
            self.cl_play.hide()

    def slot_play_pause(self):
        """ 播放/暂停 连接的槽 """
        self.playing = not self.playing
        self.update()
        self.signal_play.emit(self.playing)

    def slot_pre(self):
        """ 上一曲 连接的槽 """
        self.signal_pre.emit()

    def slot_next(self):
        """ 下一曲 连接的槽 """
        self.signal_next.emit()


class ProgressBar(QFrame):
    """
    进度条
    """
    # 进度条被鼠标点击、拖拽产生的信号
    signal_rate_changed = pyqtSignal(float)

    # 进度拖动点击的信号
    def __init__(self, parent=None):
        """
        初始化
        :param parent: 父窗体
        """
        super().__init__(parent)
        # 是否鼠标点击了，拖拽事件时调用
        self.clicked = False
        # 当前进度
        self.rate = 0
        # 是否加载完成
        self.loaded = False
        self.in_radius = playbar_progress_ir
        self.out_radius = playbar_progress_or
        # 一直监听鼠标事件
        self.setMouseTracking(True)

    def calc_rate(self, event):
        """
        更新进度
        :param event:鼠标点击事件的参数
        """
        x = event.x()
        if x > self.out_radius and self.loaded:
            if x < self.width() - self.out_radius:
                self.rate = (x - self.out_radius) / (self.width() - 2 * self.out_radius)
                self.signal_rate_changed.emit(self.rate)
                self.update()

    def mousePressEvent(self, event):
        self.clicked = True
        self.calc_rate(event)

    def mouseMoveEvent(self, event):
        if self.clicked:
            self.calc_rate(event)

    def mouseReleaseEvent(self, event):
        self.clicked = False

    def enterEvent(self, event):
        if self.loaded:
            self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        """
        重写绘制事件，自己绘图
        :param event: 绘图事件
        """
        d_r = self.out_radius - self.in_radius
        w = self.width() - 2 * self.out_radius

        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        if self.loaded:
            color1 = load_color
            color2 = in_color
        else:
            color1 = base_color
            color2 = load_color
        # 绘制进度条基础
        painter.setPen(Qt.NoPen)
        painter.setBrush(color1)
        rect = QRect(d_r, d_r, w + 2 * self.in_radius, self.in_radius * 2)
        painter.drawRoundedRect(rect, self.in_radius, self.in_radius)
        # 绘制加载进度条
        painter.setPen(Qt.NoPen)
        painter.setBrush(color2)
        rect = QRect(d_r, d_r, w * self.rate + 2 * self.in_radius, self.in_radius * 2)
        painter.drawRoundedRect(rect, self.in_radius, self.in_radius)

        if self.loaded:
            # 绘制进度条节点外圆
            painter.setPen(Qt.NoPen)
            painter.setBrush(out_color)
            painter.drawEllipse(w * self.rate, 0, 2 * self.out_radius, 2 * self.out_radius)
            # 绘制进度条节点内圆
            painter.setPen(Qt.NoPen)
            painter.setBrush(in_color)
            painter.drawEllipse(w * self.rate + d_r, d_r, 2 * self.in_radius, 2 * self.in_radius)


class ProgressGroup(QFrame):
    """
    进度组件
    包含控件:当前时间标签，总时间标签和进度条
    """
    # 进度改变信号，由鼠标点击或拖拉进度条产生
    signal_rate_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.c_time = 0
        self.t_time = 0

        self.progress_bar = ProgressBar(self)
        self.cur_time = QLabel(self)
        self.total_time = QLabel(self)

        fm = self.cur_time.fontMetrics()
        self.w, self.h = fm.width('00000'), fm.height()

        self.init_components()
        self.signal_slot()

    def init_components(self):
        """ 初始化组件 """
        style = "color:#80FFFFFF;"
        self.setMinimumHeight(self.h)
        self.cur_time.setText('00:00')
        self.cur_time.setAlignment(Qt.AlignCenter)
        self.total_time.setText('00:00')
        self.total_time.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(style)

    def signal_slot(self):
        """ 连接信号和槽 """
        self.progress_bar.signal_rate_changed.connect(self.signal_rate_changed.emit)

    def slot_cur_time(self, x):
        """ 更新当前时间 """
        if self.progress_bar.loaded:
            m = x // 1000 // 60
            s = x // 1000 - 60 * m
            self.cur_time.setText("%02d:%02d" % (m, s))
            rate = x / (self.t_time + 1)
        else:
            rate = x
        self.progress_bar.rate = rate
        self.progress_bar.update()

    def slot_total_time(self, x):
        """ 更新总时间 """
        m = x // 1000 // 60
        s = x // 1000 - 60 * m
        self.total_time.setText("%02d:%02d" % (m, s))
        self.t_time = x

    def slot_loaded(self, loaded):
        """ 更新加载状态 """
        self.progress_bar.loaded = loaded

    def resizeEvent(self, event):
        # 设置两个标签大小
        self.cur_time.setGeometry(0, 0, self.w, self.h)
        self.total_time.setGeometry(self.width() - self.w, 0, self.w, self.h)
        # 设置进度条的大小
        r = self.progress_bar.out_radius
        self.progress_bar.setGeometry(self.w, self.h / 2 - r, self.width() - self.w * 2, r * 2)


class Player:
    def __init__(self):
        self.player = QMediaPlayer()
        self.list = []

    def slot_next(self):
        pass

    def slot_pre(self):
        pass


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


class VolumeButton(AwesomeLabel):
    """
    声音控制组件
    自身(self)点击(clicked)时，计算弹窗的位置并显示
    """
    # 声音改变的信号
    signal_volume_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent, 'volume_btn', '\uf027', 30)
        self.muted = False

        self.pop_volume = PopFrame()
        self.sli_volume = QSlider(self.pop_volume)
        self.cl_volume = AwesomeLabel(self.pop_volume, 'cl_volume', '\uf027', 20)

        self.init_components()
        self.signal_slot()

    def init_components(self):
        style = """
            #btn_volume {color:#FFFFFF;}
            #btn_volume:hover {color:#%s;}
        """ % theme_color
        x = 30
        self.setFixedSize(x, x)
        self.setObjectName('btn_volume')
        self.sli_volume.setGeometry(self.width() / 2 - 10, 10, 20, 60)
        self.sli_volume.setOrientation(Qt.Vertical)
        self.sli_volume.setObjectName('sli_volume')
        self.cl_volume.setGeometry(self.width() / 2 - 10, 72, 20, 20)
        self.cl_volume.setObjectName('cl_volume')
        self.setStyleSheet(style)

    def signal_slot(self):
        self.clicked.connect(self.slot_calc_pos)
        self.cl_volume.clicked.connect(self.slot_mute)
        self.sli_volume.valueChanged.connect(self.slot_volume)

    def slot_calc_pos(self):
        """ 计算声音修改弹窗的位置，让其跟随声音图标位置显示 """
        pos = self.parent().mapToGlobal(self.pos())
        # pos = self.pos()
        self.pop_volume.setGeometry(pos.x(), pos.y() - 100, self.width(), 100)
        self.pop_volume.show()

    def slot_mute(self):
        """ 声音静音 """
        self.muted = not self.muted
        if self.muted:
            self.cl_volume.setText('\uf026')
            self.signal_volume_changed.emit(0)
        else:
            self.slot_volume(self.sli_volume.value())
        logging.debug("[静音]:%s -> %s" % (not self.muted, self.muted))

    def slot_volume(self, x):
        """
        声音改变
        :param x: 该变量
        """
        if x > 80:
            self.cl_volume.setText('\uf028')
        elif x > 0:
            self.cl_volume.setText('\uf027')
        else:
            self.cl_volume.setText('\uf026')
        self.signal_volume_changed.emit(x)
        logging.debug("[声音改变]: -> %s" % (x))


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
        self.qqmusic.clicked.connect(lambda : self.signal_play.emit(self.song, True))
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
