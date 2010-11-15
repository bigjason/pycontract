import re
from pycontract.exceptions import ValidationError

class RegexValidator(object):
    
    def __init__(self, regex=None):
        self.regex = re.compile(regex)
        
    def __call__(self, value):
        if not self.regex.search(value):
            raise ValidationError('Input did not match supplied regex "%s".' % self.regex.pattern)
        
def validate_integer(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError('Not a valid integer.')