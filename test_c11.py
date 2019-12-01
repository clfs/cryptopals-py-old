# 11. An ECB/CBC detection oracle
import lib.oracles as oracles

from test_c08 import is_aes_ecb_ct


def detect_mode(ct: bytes) -> str:
    return "ECB" if is_aes_ecb_ct(ct) else "CBC"


def test_solution():
    oracle = oracles.EcbOrCbc()

    for _ in range(100):
        ct = oracle.query(bytes(50))
        want = oracle._last_mode
        got = detect_mode(ct)
        assert want == got