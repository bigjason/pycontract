import abc
import sys
import collections
from datetime import datetime

from dateutil import parser

from pycontract.exceptions import UnableToCleanError, ValidationError

class BaseField(object):
    """
    A field represents one unit of data on the DataContract.
    
    The default value can be a callable function.
    
    Note that the name is assigned at runtime when the datacontract class is created and is included for convenience only.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, order=None, null=True, default=None, label=None, processors=[], validators=[]):

        self.order = order
        self.null = null
        self.default = default
        self.label = label
        self.processors = processors
        self.validators = validators

        # Calculated fields
        self.name = ""
        
    def _get_default(self):
        if self.default:
            if isinstance(self.default, collections.Callable):
                return self.default()
            else:
                return self.default
        else:
            return None 

    def _prepare_value(self, value):
        """
        Called when the user calls is_valid().  This is where values are processed and prepared
        for use.
        """
        result = self._process(value)
        if result == None:
            result = self._get_default()
        result = self.clean(result)
        self._validate(result)
        return result

    def _process(self, value):
        """
        Runs all processors for this field.
        """
        result = value
        for processor in self.processors:
            result = processor(result)

        return result

    def _apply_field_override(self, o):

        order = o.pop("order", None)
        default = o.pop("default", None)
        label = o.pop("label", None)
        processors = o.pop("processors", None)
        validators = o.pop("validators", None)

        if len(o) > 0:
            raise AttributeError("Unrecognized parameter(s) in field_override for field '%s'." % self.name)

        if order: self.order = order
        if default: self.default = default
        if label: self.label = label
        if processors: self.processors = processors
        if validators: self.validators = validators

    @abc.abstractmethod
    def clean(self, value):
        """
        Converts value to the final value format/type.  Raises UnableToCleanError if
        the conversion fails.
        """
        pass

    def _validate(self, value):
        """
        Runs all validators for this field.
        """
        if not self.null and value == None:
            raise ValidationError("Null value not allowed.")

        for validator in self.validators:
            validator(value)
            
    def get_display(self):
        return self.label.title()

    def __repr__(self):
        return "<Field: 'Field Name: {}'".format(self.name)

    def __str__(self):
        return "Field Name: {}".format(self.name)


class StringField(BaseField):

    def __init__(self, *args, **kwargs):

        super(StringField, self).__init__(*args, **kwargs)

    def clean(self, value):

        cleaned = str(value) if value != None else value

        return cleaned

class NumberField(BaseField):

    def clean(self, value):
        try:
            cleaned = int(value) if value != None else value
        except:
            raise UnableToCleanError("Unable to clean number value.")
        return cleaned

class IntField(BaseField):
    MAX_INT = sys.maxint
    MIN_INT = -sys.maxint - 1
    
    def clean(self, value):
        cleaned = None
        try:
            cleaned = int(value) if value != None else value
        except:
            raise UnableToCleanError("The value '%s' is not a valid int." % str(value))
        
        if cleaned != None and (cleaned > self.MAX_INT or cleaned < self.MIN_INT):
            raise UnableToCleanError("The value is outside the bounds of an int.")
        
        return cleaned
    
class LongField(BaseField):
    
    def clean(self, value):
        try:
            cleaned = long(value) if value != None else value
        except:
            raise UnableToCleanError("Unable to clean number value.")
        return cleaned
        

class BooleanField(BaseField):

    def clean(self, value):
        try:
            cleaned = bool(value) if value != None else value
        except:
            raise UnableToCleanError("Unable to clean boolean value.")
        return cleaned

class DateTimeField(BaseField):

    def clean(self, value):
        if isinstance(value, datetime):
            return value
        else:
            return parser.parse(str(value))

class ContractField(BaseField):
    """
    A field that contains a single DataContract.  This is equivalent to a one to one relationship in a database.
    """

    def clean(self, value):
        return value

    def _validate(self, value):
        """Override the _validate to call _validate on the fields of the datacontract child."""
        for field in value.fields:
            field._validate()
            
class ContractListField(BaseField):
    """
    A field that contains multiple DataContract objects.  This is equivalent to a one to many relationship in a database.
    """
    
    def clean(self, value):
        return value
    
    def _validate(self, value):
        for contract in value:
            for field in contract.fields:
                field._validate()