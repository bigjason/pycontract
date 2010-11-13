import unittest
import datetime

from pycontract.field import Field

class DataContractTester(DataContract):
    
    string_value = Field(null=False, types=(str,))
    int_value = Field(null=True, types=(int,))
    date_value = Field(null=False, types=(datetime.datetime,))
    
    default_value = Field(null=False, types=(str,), default="I am a string!")
    
class DataContractChildTester(DataContractTester):
    
    bool_value = Field(null=False, types=(bool,))

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
        
        self.assertEqual(tester["string_value"], STRING_VAL)
        self.assertEqual(tester["int_value"], INT_VAL)
        self.assertEqual(tester["date_value"], DATE_VAL)

    def test_init_with_bad_values(self):
        
        with self.assertRaises(KeyError):
            DataContractTester(madeupvalue="Anything")

    def test_init_of_fields(self):
        
        tester = DataContractTester()
        
        for field in tester.fields.itervalues():
            self.assertIsInstance(field, Field)
            self.assertIsNotNone(field.name)
            self.assertIsNotNone(field.types)

    def test_datacontract_len(self):
        
        tester = DataContractTester()
        self.assertGreater(len(tester), 3)
        
    def test_inheritence(self):
        STRING_VAL = "Test string"
        BOOL_VAL = True
        tester = DataContractChildTester(string_value=STRING_VAL, bool_value=BOOL_VAL)

        self.assertEqual(tester["string_value"], STRING_VAL)
        self.assertEqual(tester["bool_value"], BOOL_VAL)
        
    def test_label_auto(self):
        
        tester = DataContractTester()
        for field in tester.fields.itervalues():
            self.assertEqual(field.name, field.label)
            
    def test_label_manual(self):
        LABEL_TEXT = "Label Here"
        class DCLabelTester(DataContract):
            not_label = Field(label=LABEL_TEXT)
            
        tester = DCLabelTester() 
        self.assertNotEqual(tester.fields["not_label"].name, tester.fields["not_label"].label)
        self.assertEqual(tester.fields["not_label"].label, LABEL_TEXT)
