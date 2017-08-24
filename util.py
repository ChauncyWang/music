import json
import sqlite3
import task_thread


def dict_adapter(dic, *args):
    result = None
    for arg in args:
        if result is None:
            result = dic.get(arg)
    return result


class Configuration:
    config = None

    @staticmethod
    def get(*args):
        default = args[0]
        result = Configuration.config.get(args[1])
        try:
            for arg in args[2:]:
                result = result.get(arg)
            return result
        except Exception:
            return default

    @staticmethod
    def load_config():
        file = open('appdata.json', 'r').read()
        Configuration.config = json.loads(file)

    @staticmethod
    def save_config():
        file = open('appdata.json', 'w')
        file.write(json.dumps(Configuration.config))
