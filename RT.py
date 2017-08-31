import ctypes

ll = ctypes.cdll.LoadLibrary
path = "music_ui/cmake-build-debug/libmusic_ui.so"

lib = ll(path)

lib.Hello()