import Cryptodome.Util.strxor as strxor

import lib.bitops as bitops
import lib.reshape as reshape


def find_single_xor_key(ct: bytes) -> int:
    common_chars = set(b" etaoin")

    def heuristic(k: int) -> int:
        # 1 point for every common character in the resulting plaintext.
        return sum(1 for b in strxor.strxor_c(ct, k) if b in common_chars)

    return max(range(256), key=heuristic)


def find_repeating_xor_key(ct: bytes, min_len: int = 2, max_len: int = 40) -> bytes:
    def heuristic(ks: int) -> int:
        # The sum of Hamming distances between consecutive key-sized chunks.
        pairs = reshape.pairs(reshape.blocks(ct, ks))
        return sum(bitops.hamming_dist(x, y) for x, y in pairs if len(x) == len(y))

    key_size = min(range(min_len, max_len + 1), key=heuristic)
    return bytes(find_single_xor_key(ct[i::key_size]) for i in range(key_size))
