from PyQt5.QtCore import QUrl, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

from core import download_img, SONG, download_mp3
from models import Song
from ui.awesome import *
from ui.components.base_component import *
from ui.components.lyric import Lyric
from ui.config import *


class PlayBar(QFrame):
    """
    音乐播放器下边的播放栏
    """

    def __init__(self, core, parent):
        super().__init__(parent)
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




class PlayButton(ClickableLabel):
    PLAY = 1
    PAUSE = 2
    PRE = 3
    NEXT = 4
    texts = {PLAY: icon_play, PAUSE: icon_pause, PRE: icon_step_backward, NEXT: icon_step_forward, }

    @staticmethod
    def new_label(kind, parent, size):
        if kind == PlayButton.PLAY:
            # label = PlayButton(size, parent, size // 20)
            label = ClickableLabel(parent)
            label.setStyleSheet("font: 14px 'FontAwesome';color:#FFFFFF;")
            label.setObjectName("play_play")
            label.setText(icon_play)
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
