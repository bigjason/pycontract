import unittest
from datetime import datetime, date

from pycontract.fields import *
from pycontract.exceptions import UnableToCleanError, ValidationError
from pycontract.contract import DataContract

class TestDataField(unittest.TestCase):

    def test_null(self):
        field = StringField(null=False)
        self.assertEqual(field._prepare_value("I am a string"), "I am a string")

        field.null = False
        with self.assertRaises(ValidationError):
            field._prepare_value(None)
            
    def test_default_callable(self):
        expected = "Test Value"
        class Dummy(DataContract):
            callable = StringField(default=lambda: expected)
            
        tester = Dummy()
        self.assertEqual(tester.callable, expected)
        
    def test_default_value(self):
        expected = 1002
        class Dummy(DataContract):
            val = IntField(default=expected)
            
        tester = Dummy()
        self.assertEqual(tester.val, expected)

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

class TestIntField(unittest.TestCase):
    def setUp(self):
        self.field = IntField()

    def tearDown(self):
        del self.field
    
    def test_normal_int(self):
        self.assertEqual(self.field.clean(12), 12)
        
    def test_str_values(self):
        values = (
            ("123", 123),
            ("-123", -123),
        )
        
        for input, expected in values:
            self.assertEqual(self.field.clean(input), expected, "Value '%s' had an error." % input)
            
    def test_long_failure(self):
        
        with self.assertRaises(UnableToCleanError):
            self.field.clean("324234234234234234234234")
        
        with self.assertRaises(UnableToCleanError):
            self.field.clean(324234234234234234234234)
      