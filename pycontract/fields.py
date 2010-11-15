import abc

from pycontract.exceptions import UnableToCleanError, ValidationError

class BaseField(object):
    """
    A field represents one unit of data on the DataContract.
    
    Note that the name is assigned at runtime when the datacontract class is created and is included for convenience only.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, null=True, default=None, label=None, processors=[], validators=[]):

        self.null = null
        self.default = default
        self.label = label
        self.processors = processors
        self.validators = validators

        # Calculated fields
        self.name = ""

    def prepare_value(self, value):
        """
        Called when a field is set.
        """
        result = self.process(value)
        result = self.clean(result)
        self.validate(result)
        return result

    def process(self, value):
        """
        Runs all processors for this field.
        """
        result = value
        for processor in self.processors:
            result = processor(result)

        return result
    
    def apply_field_override(self, o):
        
        default = o.pop("default", None)
        label = o.pop("label", None)
        processors = o.pop("processors", None)
        validators = o.pop("validators", None)
        
        if len(o) > 0:
            raise AttributeError("Unreconized parameter(s) in field override for field '%s'." % self.name)
        
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

    def validate(self, value):
        """
        Runs all validators for this field.
        """
        if not self.null and value == None:
            raise ValidationError("Null value not allowed.")
             
        for validator in self.validators:
            validator(value)

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
    
class BooleanField(BaseField):
    
    def clean(self, value):
        try:
            cleaned = bool(value) if value != None else value
        except:
            raise UnableToCleanError("Unable to clean boolean value.")
        return cleaned

class DateTimeField(BaseField):
    
    def clean(self, value):
        return value