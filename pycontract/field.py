import abc

from pycontract.exceptions import UnableToCleanError

class BaseField(object):
    """
    A field represents one unit of data on the DataContract.
    
    Note that the name is assigned at runtime when the datacontract class is created and is included for convenience only.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, null=True, default=None, label=None):

        self.null = null
        self.default = default
        self.label = label

        # Calculated fields
        self.name = ""

    @abc.abstractmethod
    def clean(self, value):
        pass

    def __repr__(self):
        return "<Field: 'Field Name: {}'".format(self.name)

    def __str__(self):
        return "Field Name: {}".format(self.name)


class StringField(BaseField):

    def __init__(self, *args, **kwargs):

        self.max_length = kwargs.pop("max_length", None)
        self.max_length_trim = kwargs.pop("max_length_raise", False)
        self.strip = kwargs.pop("strip", True)

        super(StringField, self).__init__(*args, **kwargs)

    def clean(self, value):
        cleaned = str(value or "")
        
        if self.strip:
            cleaned = cleaned.strip()

        if self.max_length:
            if self.max_length_trim:
                cleaned = cleaned[:self.max_length]
            else
                if len(cleaned) > self.max_length:
                    raise UnableToCleanError("Length of value is too long.  Expected {}, received {}".format(self.max_length, len(cleaned)))
                
        return cleaned
    
class NumberField(BaseField):

    def __init__(self, *args, **kwargs):

        self.max_value = kwargs.pop("max_value", None)
        self.min_value = kwargs.pop("min_value", None)
        self.try_cleanup = kwargs.pop("try_cleanup", True)

        super(StringField, self).__init__(*args, **kwargs)

    def clean(self, value):
        cleaned = value
        if self.try_cleanup:
            numbers = []
            for c in cleaned:
                if c.isdigit():
                    numbers.append(c)
            cleaned = "".join(numbers)
            
        try:
            cleaned = int(cleaned)
        except:
            raise UnableToCleanError("Unable to clean the values.")