from PyQt5.QtGui import QColor

theme_color = '80FF0066'

foreground_color = QColor.fromRgba(int(theme_color, 16))
base_color = QColor(255, 255, 255)
load_color = QColor(180, 180, 180)
in_color = foreground_color
out_color = QColor(255, 255, 255)

# PlayBar
playbar_h = 60
# PlayButtons
playbar_playbtns_w = 180
playbar_playbtns_big = 50
playbar_playbtns_small = 30

# ProgressBar
# 进度点内圆半径
playbar_progress_ir = 1
# 进度点外圆半径
playbar_progress_or = 4
