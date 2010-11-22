"""
For more ready to validators, see the django project.
"""

import re
from pycontract.exceptions import ValidationError

class RegexValidator(object):

    def __init__(self, regex=None):
        self.regex = re.compile(regex)

    def __call__(self, value):
        if not self.regex.search(str(value)):
            raise ValidationError('Input did not match supplied regex: "%s".' % self.regex.pattern)

valid_number = RegexValidator(r"^-?\d+(\.\d+)?$")
