import ctypes
from ctypes import byref

ll = ctypes.cdll.LoadLibrary
path = "music_ui/cmake-build-debug/libmusic_ui.so"

lib = ll(path)


def add(x, y):
    return x + y


lib.callback(byref(add))

