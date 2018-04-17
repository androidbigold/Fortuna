from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class Generator:
    block_size = AES.block_size
    key_size = 32

    def __init__(self):
        self.counter = Counter.new(nbits=self.block_size * 8, initial_value=0, little_endian=True)
        self.key = None

    def reseed(self, seed):
        """
        reset seed
        :param seed: new seed
        """
        if self.key is None:
            self.key = b'\0' * self.key_size
        self._set_key(SHA256.new(SHA256.new(self.key + seed).digest()).digest())
        self.counter()

    def _set_key(self, key):
        """
        :param key: new key
        """
        self.key = key
        self._cipher = AES.new(key, AES.MODE_CTR, counter=self.counter)

    def _generateblocks(self, n):
        """
        generate AES encrypt data block(fake random byte string)
        :param n: n blocks to generate
        :return: 16n bytes fake random byte string
        """
        if self.key is None:
            raise AssertionError('generator must be seeded before use')
        result = b''
        for i in range(n):
            result += self._cipher.encrypt(self.counter())
        return result

    def pseudorandomdata(self, n):
        """
        generate random data
        :param n: n bytes to generate
        :return: n bytes random data
        """
        if n < 0 or n > 2 ** 20:
            raise ValueError('byte number is out of range(0 <= n <= 2^20)')
        result = self._generateblocks(n // 16 if n % 16 == 0 else (n // 16) + 1)[:n]
        self.key = self._generateblocks(2)

        return result
