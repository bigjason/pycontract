

class Field(object):
    """
    A field represents one field of data on the DataContract.
    
    Note that the name is assigned at runtime when the datacontract class is created.
    """

    def __init__(self, null=True, types=(), default=None, label=None):
        if not isinstance(types, tuple):
            raise ValueError("types parameter must be a tuple.")

        self.null = null
        self.types = types
        self.default = default
        self.label = label

        # Calculated fields
        self.name = ""

    def is_valid(self, value):
        if not self.null and value == None:
            return False

        if value != None and len(self.types) > 0:
            if type(value) not in self.types:
                return False

        return True

    def __repr__(self):
        return "<Field: 'Field Name: {0}'".format(self.name)

    def __str__(self):
        return "Field Name: {0}".format(self.name)

def StrField(**kwargs):
    kwargs["types"] = (str,)
    return Field(**kwargs)

def IntField(**kwargs):
    kwargs["types"] = (int,)
    return Field(**kwargs)

def BoolField(**kwargs):
    kwargs["types"] = (bool,)
    return Field(**kwargs)    
