import os
import unittest

from utils.misc import zfill, replace_char, is_monochar, generate_packet, \
    round_to_next_multiple


class TestMisc(unittest.TestCase):

    def test_zfill(self):
        s = "test"
        z = zfill(s, 9)

        self.assertEqual("00000test", z)

        w = zfill(s, 2)
        self.assertEqual(s, w)

    def test_replace_char(self):
        s = "1001111"
        z = replace_char(s, 2, '1')

        self.assertEqual("1011111", z)

        s = "1001111"
        z = replace_char(s, 10, '1')

        self.assertEqual(s + '1', z)

    def test_is_monochar(self):
        s = "1111111"

        self.assertTrue(is_monochar(s))
        self.assertTrue(is_monochar(s), '1')
        self.assertFalse(is_monochar(s, '0'))

        s = ''

        self.assertFalse(is_monochar(s))

    def test_generate_packet(self):
        s = generate_packet(40)

        self.assertEqual(40, len(s))

        _ = generate_packet(1000, 'debug/packet')

        with open("debug/packet", 'r', encoding="utf-8") as f:
            p = f.read()

        self.assertEqual(1000, len(p))

        os.remove('debug/packet')

    def test_next_multiple(self):
        self.assertEqual(14, round_to_next_multiple(8, 7))
        self.assertEqual(14, round_to_next_multiple(14, 7))
        self.assertEqual(21, round_to_next_multiple(15, 7))
        self.assertEqual(0, round_to_next_multiple(0, 7))
        self.assertEqual(-14, round_to_next_multiple(-20, 7))
