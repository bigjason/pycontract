import unittest

from pycontract.field import Field


class TestDataField(unittest.TestCase):

    def test_init_types(self):
        with self.assertRaises(ValueError):
            Field(types=[str])

    def test_is_valid_null(self):
        field = Field(null=False)
        self.assertTrue(field.is_valid("I am a string"))

        field.null = True
        self.assertTrue(field.is_valid(None))

        field.null = False
        self.assertFalse(field.is_valid(None))

    def test_is_valid_type(self):
        field = Field(null=False, types=(int, str,))

        self.assertTrue(field.is_valid("String Value"))
        self.assertTrue(field.is_valid(231))
        self.assertFalse(field.is_valid(False))
        