import unittest
import random
from groundstation.ue_encoder import UnambiguousEncoder

class TestUnambiguousEncapsulation(unittest.TestCase):

    test_bytes = [0b01010101, 0b11110000]
    test_message = [31, 54, 31, 54, 31, 54, 31, 54, 54, 54, 54, 54, 31, 31, 31, 31]
    test_header = [41, 0, 41, 0, 41, 0, 41, 0, 0, 0, 0, 0, 41, 41, 41, 41]

    def test_successfully_encoded(self):
        # Create an encoder with the default codes
        encoder = UnambiguousEncoder()

        # Try encoding with the message code
        message = encoder.encode("message", self.test_bytes)
        header  = encoder.encode("header", self.test_bytes)

        # These offsets are totes legit. Trust me.
        self.assertEqual(message, self.test_message)
        self.assertEqual(header,  self.test_header)

    def test_successfully_decoded(self):
        encoder = UnambiguousEncoder()

        message = encoder.decode("message", self.test_message)
        header  = encoder.decode("header", self.test_header)

        self.assertEqual(message, self.test_bytes)
        self.assertEqual(header,  self.test_bytes)

    @staticmethod
    def flip_n_bits(n, msg):
        out = []
        for byte in msg:
            bits = list(range(8))
            for _ in range(n):
                bit = bits.pop(random.randint(0, len(bits) - 1))
                byte = byte ^ 1 << bit
            out.append(byte)
        return out

    def test_1_flipped_bit(self):
        encoder = UnambiguousEncoder()

        flipped_message = self.flip_n_bits(1, self.test_message)
        message = encoder.decode("message", flipped_message)

        self.assertEqual(message, self.test_bytes)

    def test_decode_weird_lengths(self):
        encoder = UnambiguousEncoder()

        message = encoder.decode("message", self.test_message + [54, 31])
        test_bytes = self.test_bytes + [0b00000010]
        self.assertEqual(message, test_bytes)
