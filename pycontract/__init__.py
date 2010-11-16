from pycontract.contract import DataContract
from pycontract.fields import BaseField, BooleanField, DateTimeField, NumberField, StringField
from pycontract.processors import strip_non_numeric, strip_white_space
from pycontract.validators import RegexValidator, valid_number