import threading

import core


class HttpTask(threading.Thread):

    def __init__(self, method, args, update_callback, finish_callback):
        super().__init__()

    def run(self):
        pass