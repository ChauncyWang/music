import math
import threading
from random import Random

import os
from moviepy.editor import *


def cut(file):
    video = VideoFileClip(file)
    length = math.floor(video.duration)
    for i in range(0, 10):
        begin = Random().randint(0, length - 10)
        clip = video.subclip(begin, begin + 10)
        result = CompositeVideoClip([clip, ])
        if not os.path.exists(file[:-4]):
            os.mkdir(file[:-4])
        result.write_videofile("%s/%d-%d.mp4" % (file[:-4], i, begin), codec="libx264", bitrate="5000k")


def files(path):
    return os.listdir(path)

path = "/home/hy/文档/录像晋彬"
for file in files(path):
    cut('%s/%s' % (path, file))