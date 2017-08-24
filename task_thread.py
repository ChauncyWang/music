import logging
from threading import Thread
from multiprocessing import Process

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

def task(target, callback, *args, **kwargs):
    t = TaskThread(target, callback, *args, **kwargs)
    return t


class TaskThread(QObject, Thread):
    finish = pyqtSignal(object)
    def __init__(self, target, *args, **kwargs):
        super(QObject, self).__init__()
        super(Thread, self).__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.debug("task begin...")
        result = self.target(*self.args, **self.kwargs)
        self.finish.emit(result)
        logging.debug("task end!")
