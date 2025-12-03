from typing import List
import hashlib

def fib_sequence(n: int) -> List[int]:
    if n <= 0: return []
    if n == 1: return [1]
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq

def golden_ratio() -> float:
    return (1 + 5 ** 0.5) / 2

def map_to_fib_barcode(seed: str, length: int = 10) -> str:
    base = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    fibs = fib_sequence(length + 5)
    digits = []
    for i in range(length):
        hex_pair = base[i*2:(i*2)+2]
        v = int(hex_pair, 16)
        d = (v + fibs[i]) % 10
        digits.append(str(d))
    if len(set(digits)) <= 3:
        phi = int(golden_ratio() * 100) % 10
        digits[-1] = str((int(digits[-1]) + phi) % 10)
    return "".join(digits)

seed = "Bus of Inheritance-2025-12-02"
print(map_to_fib_barcode(seed, 10))
