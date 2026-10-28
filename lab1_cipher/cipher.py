"""LFSR + bit-permutation file cipher (Lab 1). No tkinter dependency."""
import os

KEY = 0x67BD5
MASK = 0x7FFFF  # 19 bits
TAPS = (13, 16, 17, 18)  # x^14, x^17, x^18, x^19 (bit 0 is the leftmost cell, x^1)
TAP_MASK = sum(1 << t for t in TAPS)
OUT_BIT = 18

# pi(i) = j, indices 1..8 with index 1 the most significant bit
PI = {1: 2, 2: 6, 3: 3, 4: 5, 5: 1, 6: 8, 7: 4, 8: 7}
# "A": input bit at index i moves to index pi(i); "B": output bit i takes input bit pi(i)
PERMUTATION_READING = "B"


class LFSR:
    def __init__(self, seed=KEY):
        self.reg = seed & MASK

    def next_byte(self):
        reg = self.reg
        b = 0
        for i in range(8):
            b |= ((reg >> OUT_BIT) & 1) << i
            fb = bin(reg & TAP_MASK).count("1") & 1
            reg = ((reg << 1) & MASK) | fb
        self.reg = reg
        return b

    def stream(self, n):
        return bytes(self.next_byte() for _ in range(n))


def permute_byte(b, mapping):
    out = 0
    for i, j in mapping.items():
        if (b >> (8 - i)) & 1:
            out |= 1 << (8 - j)
    return out


def _tables(reading):
    mapping = PI if reading == "A" else {j: i for i, j in PI.items()}
    perm = [permute_byte(b, mapping) for b in range(256)]
    inv = [0] * 256
    for b, p in enumerate(perm):
        inv[p] = b
    return perm, inv


PERM, INV = _tables(PERMUTATION_READING)


def encrypt_bytes(data, lfsr, perm=None):
    perm = perm or PERM
    return bytes(perm[d] ^ k for d, k in zip(data, lfsr.stream(len(data))))


def decrypt_bytes(data, lfsr, inv=None):
    inv = inv or INV
    return bytes(inv[d ^ k] for d, k in zip(data, lfsr.stream(len(data))))


def process(in_path, out_path, mode, progress=None, chunk=4096):
    """Encrypt or decrypt in_path into out_path, reporting progress(done, total)."""
    lfsr = LFSR()
    total = os.path.getsize(in_path)
    done = 0
    tmp = out_path + ".tmp"
    fn = encrypt_bytes if mode == "encrypt" else decrypt_bytes
    try:
        with open(in_path, "rb") as f, open(tmp, "wb") as g:
            while data := f.read(chunk):
                g.write(fn(data, lfsr))
                done += len(data)
                if progress:
                    progress(done, total)
        if total == 0 and progress:
            progress(0, 0)
        os.replace(tmp, out_path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return done
