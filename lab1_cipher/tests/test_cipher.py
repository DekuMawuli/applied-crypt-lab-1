import os
import random
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import cipher

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


class CipherTests(unittest.TestCase):
    def test_permutation_bijection(self):
        self.assertEqual(sorted(cipher.PERM), list(range(256)))
        for b in range(256):
            self.assertEqual(cipher.INV[cipher.PERM[b]], b)

    def test_permutation_single_bit(self):
        # reading B: output index 1 (MSB) takes input index pi(1)=2 (0x40)
        self.assertEqual(cipher.PERM[0x40], 0x80)

    def test_seed_bits_out_msb_first(self):
        l = cipher.LFSR()
        bits = []
        for _ in range(7):
            bits.append((l.reg >> 18) & 1)
            l.reg = ((l.reg << 1) & cipher.MASK) | 0
        self.assertEqual(bits, [1, 1, 0, 0, 1, 1, 1])
        # first output byte: first bit is the LSB
        self.assertEqual(cipher.LFSR().next_byte() & 0x7F, 0b1110011)
        # bits out 1,1,0,0,1,1,1,1 with the first as the LSB, worked by hand
        self.assertEqual(cipher.LFSR().next_byte(), 0xF3)

    def test_zeros_give_keystream(self):
        self.assertEqual(cipher.encrypt_bytes(bytes(32), cipher.LFSR()), cipher.LFSR().stream(32))

    def test_round_trip_and_chunking(self):
        rnd = random.Random(1)
        for n in (0, 1, 100, 65535, 65536, 65537, 200000):
            data = bytes(rnd.randrange(256) for _ in range(n))
            with tempfile.TemporaryDirectory() as d:
                src, enc, dec = (os.path.join(d, x) for x in ("s", "e", "d"))
                open(src, "wb").write(data)
                cipher.process(src, enc, "encrypt")
                cipher.process(enc, dec, "decrypt", chunk=1000)
                self.assertEqual(open(dec, "rb").read(), data)
                enc2 = os.path.join(d, "e2")
                cipher.process(src, enc2, "encrypt", chunk=777)
                self.assertEqual(open(enc, "rb").read(), open(enc2, "rb").read())

    def test_instructor_image(self):
        p = os.path.join(ROOT, "image1.jpg.enc")
        if not os.path.exists(p):
            self.skipTest("instructor image not present")
        out = cipher.decrypt_bytes(open(p, "rb").read(), cipher.LFSR())
        self.assertTrue(out.startswith(b"\xff\xd8\xff"))
        self.assertTrue(out.endswith(b"\xff\xd9"))


if __name__ == "__main__":
    unittest.main()
