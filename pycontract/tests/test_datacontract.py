import unittest
import datetime

from pycontract.fields import BaseField, StringField, NumberField, BooleanField, DateTimeField
from pycontract.contract import DataContract

class DataContractTester(DataContract):

    string_value = StringField(null=False)
    int_value = NumberField(null=True)
    date_value = DateTimeField(null=False)

    default_value = StringField(null=False, default="I am a string!")

class DataContractChildTester(DataContractTester):

    bool_value = BooleanField(null=False)

class TestDataContract(unittest.TestCase):

    def test_init(self):

        tester = DataContractTester()

        self.assertGreater(len(tester), 0)
        self.assertIsNotNone(tester.fields)

    def test_init_with_values(self):
        STRING_VAL = "Test string"
        INT_VAL = 12345
        DATE_VAL = datetime.datetime.now()
        tester = DataContractTester(string_value=STRING_VAL, int_value=INT_VAL, date_value=DATE_VAL)

        self.assertEqual(tester.string_value, STRING_VAL)
        self.assertEqual(tester.int_value, INT_VAL)
        self.assertEqual(tester.date_value, DATE_VAL)

    def test_init_with_bad_values(self):

        with self.assertRaises(KeyError):
            DataContractTester(madeupvalue="Anything")

    def test_init_of_fields(self):

        tester = DataContractTester()

        for field in tester.fields.itervalues():
            self.assertIsInstance(field, BaseField)
            self.assertIsNotNone(field.name)

    def test_datacontract_len(self):

        tester = DataContractTester()
        self.assertGreater(len(tester), 3)

    def test_inheritence(self):
        STRING_VAL = "Test string"
        BOOL_VAL = True
        tester = DataContractChildTester(string_value=STRING_VAL, bool_value=BOOL_VAL)

        self.assertEqual(tester.string_value, STRING_VAL)
        self.assertEqual(tester.bool_value, BOOL_VAL)

    def test_label_auto(self):

        tester = DataContractTester()
        for field in tester.fields.itervalues():
            self.assertEqual(field.name, field.label)

    def test_label_manual(self):
        LABEL_TEXT = "Label Here"
        class DCLabelTester(DataContract):
            not_label = StringField(label=LABEL_TEXT)

        tester = DCLabelTester()
        self.assertNotEqual(tester.fields["not_label"].name, tester.fields["not_label"].label)
        self.assertEqual(tester.fields["not_label"].label, LABEL_TEXT)

    def test_field_order(self):
        class OrderTester(DataContract):
            AField = StringField(2)
            BField = StringField(1)

        self.assertEqual(OrderTester.fields.popitem(last=False)[0], "BField")
        self.assertEqual(OrderTester.fields.popitem(last=False)[0], "AField")
