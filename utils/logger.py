import sys


class Logger(object):
    def __init__(self, filename="../log/log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding='utf-8')
        self.log.seek(0)
        self.log.truncate()  # 清空文件

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
