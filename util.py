import sqlite3
import threading


def task(callback):
    """
    任务装饰器，使用此装饰器可以开启一个线程来执行相关任务
    :param callback: 任务执行完成的回调函数
    :return:第一层装饰器
    """

    def _wrapper(method):
        """
        这里是装饰器第一层
        :param method: 开启新线程要执行的函数
        :return: 装饰器第二层
        """

        def __wrapper(*args, **kwargs):
            """
            装饰器第二层
            :param args:method 方法要调用的参数
            :param kwargs:method 方法要调用的参数
            """
            thread = TaskThread(method, callback, *args, **kwargs)
            thread.run()

        return __wrapper

    return _wrapper


class TaskThread(threading.Thread):
    """
    task 装饰器辅助的多线程类
    """

    def __init__(self, method, handle, *args, **kwargs):
        super(threading.Thread, self).__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.handle = handle

    def run(self):
        re = self.method(*self.args, **self.kwargs)
        self.handle(re)


def dict_adapter(dic, *args):
    result = None
    for arg in args:
        if result is None:
            result = dic.get(arg)
    return result


def load_db_config():
    sqlite3.connect()