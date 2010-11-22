from collections import OrderedDict

from pycontract.fields import BaseField
from pycontract.exceptions import ValidationError

class DataContractMetaClass(type):

    def __new__(cls, name, bases, attrs):
        def make_property(name):
            def getter(self):
                return self[name]
            return property(fget=getter)
        
        fields = OrderedDict()
        parents = [b for b in bases if isinstance(b, DataContractMetaClass)]
        field_overrides = attrs.pop("field_overrides", {})

        # Grab the fields of any parent classes
        for kls in parents:
            if type(kls) == DataContractMetaClass:
                for field_name in kls.fields:
                    fields[field_name] = kls.fields[field_name]

        # Grab the items for this class
        for name, value in attrs.iteritems():
            if isinstance(value, BaseField):
                value.name = name
                if not value.label:
                    value.label = name
                fields[name] = value

        # Handle any field overrides
        for name, field in fields.iteritems():
            override = field_overrides.pop(name, None)
            if override:
                field._apply_field_override(override)

        if len(field_overrides) > 0:
            raise AttributeError("One or more field_overrides did not match a field.")

        # Include all the attributes that are not BaseFields 
        newattrs = {name: value for name, value in attrs.iteritems() if not isinstance(value, BaseField)}

        #create a read-only property for each field. 
        for name in fields:
            newattrs[name] = make_property(name)

        # Sort the field order
        if len([x for x in fields if fields[x].order != None]) > 0:
            fields = OrderedDict(sorted(fields.items(), key=lambda f: f[1].order if f[1].order else f[1].label))
        else:
            fields = OrderedDict(sorted(fields.items(), key=lambda f: f[0]))

        newattrs["fields"] = fields

        return super(DataContractMetaClass, cls).__new__(cls, name, bases, newattrs)

    def __init__(self, name, bases, attrs):
        super(DataContractMetaClass, self).__init__(name, bases, attrs)


class DataContract(object):
    """
    A data contract is a declarative container of the data required for a particular function.  Values are not set with standard dot notation
    like dc.Field1 = 33, but are instead set with the set_value method or like a dictionary dc["Field1"] = 33.
    """
    __metaclass__ = DataContractMetaClass

    def __init__(self, **kwargs):
        self._data = OrderedDict()
        self._errors = {}

        # Set default values for all fields
        for name, field in self.fields.iteritems():
            self._data[name] = field._get_default()

        # Set initial values if any were provided
        for field_name in kwargs:
            self.set_value(field_name, kwargs[field_name])

    def set_value(self, field_name, field_value):
        field = self.fields.get(field_name, None)

        if field == None:
            raise KeyError("Field '%s' was not found in the fields list." % field_name)

        self._data[field.name] = field_value

    def is_valid(self):
        self._errors = {}
        for field in self.fields.itervalues():
            try:
                self.set_value(field.name, field._prepare_value(self[field.name]))
            except Exception as exc:
                self._errors[field.name] = exc.message
        return len(self._errors) == 0

    def __hash__(self):
        return super(DataContract, self).__hash__()

    ### Methods to emulate the behavior of a dictionary ###
    
    
    def itererrors(self):
        for field_name, error_message in self._errors:
            yield (field_name, error_message,)        

    def iteritems(self):
        for key, value in self._data.iteritems():
            yield (key, value,)

    def itervalues(self):
        for value in self._data.itervalues():
            yield value
            
    def iterkeys(self):
        for key in self._data.iterkeys():
            yield key

    def iterfields(self):
        for field in self.fields.itervalues():
            yield field

    def __iter__(self):
        for key in self._data:
            yield key

    def __setitem__(self, key, value):
        self.set_value(key, value)

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    ## Operator Overloads ##

    def __eq__(self, other):
        for key, value in self.iteritems():
            if value != other[key]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
