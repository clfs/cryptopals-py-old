from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
import Cryptodome.Util.strxor as strxor

import lib.bitops as bitops


class SingleXor:
    def __init__(self, k: int):
        self.k = k

    def _crypt(self, t: bytes) -> bytes:
        return strxor.strxor_c(t, self.k)

    def encrypt(self, pt: bytes) -> bytes:
        return self._crypt(pt)

    def decrypt(self, ct: bytes) -> bytes:
        return self._crypt(ct)


class RepeatingXor:
    def __init__(self, k: bytes):
        self.k = k

    def _crypt(self, t: bytes) -> bytes:
        return bitops.xor_repeat(t, self.k)

    def encrypt(self, pt: bytes) -> bytes:
        return self._crypt(pt)

    def decrypt(self, ct: bytes) -> bytes:
        return self._crypt(ct)


class AesEcb:
    def __init__(self, k: bytes):
        self.ecb = AES.new(k, AES.MODE_ECB)

    def encrypt(self, pt: bytes) -> bytes:
        return self.ecb.encrypt(Padding.pad(pt, AES.block_size))

    def decrypt(self, ct: bytes) -> bytes:
        return Padding.unpad(self.ecb.decrypt(ct), AES.block_size)
