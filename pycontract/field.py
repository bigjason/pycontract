import abc

class BaseField(object):
    """
    A field represents one field of data on the DataContract.
    
    Note that the name is assigned at runtime when the datacontract class is created.
    """

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
        return "<Field: 'Field Name: {0}'".format(self.name)

    def __str__(self):
        return "Field Name: {0}".format(self.name)
