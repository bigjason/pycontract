import unittest

from pycontract.fields import BaseField, StringField
from pycontract.exceptions import UnableToCleanError, ValidationError

class TestDataField(unittest.TestCase):

    def test_null(self):
        field = StringField(null=False)
        self.assertEqual(field.prepare_value("I am a string"), "I am a string")

        field.null = False
        with self.assertRaises(ValidationError):
            field.prepare_value(None)
        