from Generator import Generator
from Crypto.Hash import SHA256
import time


class Accumulator:
    pool_number = 32
    min_pool_size = 64
    reseed_interval = 0.1
    p = []

    def __init__(self):
        for i in range(self.pool_number):
            self.p.append(b'')
        self.ReseedCnt = 0
        self.g = Generator()
        self.last_seed = time.time()

    def randomdata(self, n):
        """
        :param n:the bytes of random data
        :return fake random byte string
        """
        if len(self.p[0]) >= self.min_pool_size or time.time() - self.last_seed > self.reseed_interval:
            self.ReseedCnt += 1
            s = b''
            for i in range(self.pool_number):
                if self.ReseedCnt % (2 ** i) == 0:
                    s += SHA256.new(SHA256.new(self.p[i]).digest()).digest()
                    self.p[i] = b''
            self.g.reseed(s)
            self.last_seed = time.time()
        return self.g.pseudorandomdata(n)

    def addrandomevent(self, s, i, e):
        """
        :param s: source number
        :param i: pool number
        :param e: subject data
        """
        assert 0 < len(e) <= 32 and 0 <= s <= 255 and 0 <= i <= 31, 'invalid parameters'
        self.p[i] = self.p[i] + (str(s) + str(len(e))).encode() + e
