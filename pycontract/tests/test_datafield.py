import unittest
from datetime import datetime, date

from pycontract.fields import BaseField, StringField, DateTimeField
from pycontract.exceptions import UnableToCleanError, ValidationError

class TestDataField(unittest.TestCase):

    def test_null(self):
        field = StringField(null=False)
        self.assertEqual(field._prepare_value("I am a string"), "I am a string")

        field.null = False
        with self.assertRaises(ValidationError):
            field._prepare_value(None)

class TestDateField(unittest.TestCase):
    
    def setUp(self):
        self.field = DateTimeField()

    def tearDown(self):
        del self.field
    
    def test_basic_string(self):
        expected = datetime(2010, 12, 30)
        actual = self.field.clean("12/30/2010")
        
        self.assertEqual(actual, expected)
        
    def test_date_time(self):
        expected = datetime(2010, 12, 30)
        actual = self.field.clean(expected)
        
        self.assertEqual(actual, expected)
    
    def test_date(self):
        value = date(1980, 1, 30)
        expected = datetime(1980, 1, 30)
        actual = self.field.clean(expected)
        
        self.assertEqual(actual, expected)

    def test_un_parsable(self):        
        
        with self.assertRaises(ValueError):
            self.field.clean("I am no date")
