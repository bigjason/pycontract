import unittest

from pycontract.processors import strip_non_numeric, strip_white_space, upper_case

class TestStripNoNumeric(unittest.TestCase):

    def test_with_string(self):

        self.assertEqual(strip_non_numeric("Bob1Bill2"), "12")

    def test_with_number(self):

        self.assertEqual(strip_non_numeric(12), "12")


class TestStripWhiteSpace(unittest.TestCase):

    def test_with_string(self):
        self.assertEqual(strip_white_space(" bob \t"), "bob")

    def test_with_int(self):
        self.assertEqual(strip_white_space(123), "123")


class TestUpperCase(unittest.TestCase):

    def test_with_string(self):
        test_str = "Test string is here  \nNow"
        self.assertEqual(upper_case(test_str), test_str.upper())

    def test_with_int(self):
        self.assertEqual(upper_case(123), "123")
