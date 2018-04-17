# 该程序只能在Linux内核下运行
from Accumulator import Accumulator
from SeedFileManage import *
from GUI import GUI
import threading
import time
import random


class seedthread(threading.Thread):
    def __init__(self, accumulator):
        threading.Thread.__init__(self)
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设为True
        self.last_seed = time.time()
        self.accumulator = accumulator
        self.seed_interval = 600
        writeseedfile(accumulator, 'seedfile')

    def run(self):
        while self.__running.isSet():
            if time.time() - self.last_seed >= self.seed_interval:
                updateseedfile(self.accumulator, 'seedfile')
                self.seed_interval = time.time()

    def stop(self):
        self.__running.clear()  # 将running设为False


class subjectthread(threading.Thread):
    def __init__(self, accumulator):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()
        self.accumulator = accumulator
        self.source = 0
        self.index = 0

    def run(self):
        while self.__running.isSet():
            with open('/dev/random', 'rb') as subject_source:
                subject_source.seek(32, 2)
                subject = subject_source.read(random.randint(1, 32))
                self.accumulator.addrandomevent(self.source, self.index, subject)
                self.source = (self.source + 1) % 256
                self.index = (self.index + 1) % 32

    def stop(self):
        self.__running.clear()


if __name__ == '__main__':
    a = Accumulator()
    try:
        f = open('seedfile', 'rb')
    except FileNotFoundError:
        with open('/dev/random', 'rb') as random_source:  # Linux内核下的设备文件，记录环境噪声，可用作随机数发生器
            random_source.seek(64, 2)
            seed = random_source.read(64)
            assert len(seed) == 64, 'Error:incorrect seed length'
    else:
        try:
            seed = f.read(64)
            assert len(seed) == 64, 'Error:incorrect seed length'
        finally:
            f.close()
    a.g.reseed(seed)
    sdthread = seedthread(a)
    sjthread = subjectthread(a)
    sdthread.start()
    sjthread.start()
    GUI(a).generateGUI()
    sdthread.stop()
    sjthread.stop()
