import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import src.sequence_editor as lib


class TestCases(unittest.TestCase):

    def test_handler_strip(self):
        self.assertEqual(
            lib.handler_strip(('1', ' 2', '3 ', ' 4 ', '5  \n', '\t6\t\n')),
            ('1', '2', '3', '4', '5', '6'))

    def test_handler_remove_duplicate(self):
        self.assertEqual(
            lib.handler_remove_duplicate(('1', '1', '2', '2', '3', '3', '2',
                                          '2', '1', '1')), ('1', '2', '3'))

    def test_handler_neighboring_duplicate(self):
        self.assertEqual(
            lib.handler_neighboring_duplicate(('1', '1', '2', '2', '3', '3',
                                               '2', '2', '1', '1')),
            ('1', '2', '3', '2', '1'))

    def test_handler_upper(self):
        self.assertEqual(lib.handler_upper(('Dong#1?',)), ('DONG#1?',))

    def test_handler_lower(self):
        self.assertEqual(lib.handler_lower(('Dong#1?',)), ('dong#1?',))

    def test_handler_zero_padding_left(self):
        self.assertEqual(
            lib.handler_zero_padding_left(('x', 'xx')), ('0x', 'xx'))

    def test_handler_zero_padding_right(self):
        self.assertEqual(
            lib.handler_zero_padding_right(('x', 'xx')), ('x0', 'xx'))

    def test_handler_dec2hex(self):
        self.assertEqual(
            lib.handler_dec2hex(('1', '16', '1000')), ('1', '10', '3e8'))

    def test_handler_hex2dec(self):
        self.assertEqual(
            lib.handler_hex2dec(('1', '10', '3e8', '3E8')),
            ('1', '16', '1000', '1000'))

    def test_handler_ascii2hex(self):
        self.assertEqual(
            lib.handler_ascii2hex(('abc', 'ABC', '123')),
            ('616263', '414243', '313233'))

    def test_handler_hex2ascii(self):
        self.assertEqual(
            lib.handler_hex2ascii(('616263', '414243', '313233', '61a', '61D')),
            ('abc', 'ABC', '123', 'a\n', 'a\r'))

    def test_handler_reverse(self):
        self.assertEqual(
            lib.handler_reverse(('Dong#1?', ' ', '')), ('?1#gnoD', ' ', ''))

    def test_handler_nonempty(self):
        self.assertEqual(
            lib.handler_nonempty(('Dong#1?', ' ', '')), ('Dong#1?', ' '))


if __name__ == '__main__':
    unittest.main()
