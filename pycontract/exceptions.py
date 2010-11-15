
class UnableToCleanError(ValueError):
    
    def __init__(self, field=None, value=None, *args, **kwargs):
        super(UnableToCleanError, self).__init__(*args, **kwargs)
        
        self.field = field
        self.value = value
        
class ValidationError(ValueError):
    pass