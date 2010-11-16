import re

rm = re.compile("[^\d]")
def strip_non_numeric(value):
    return rm.sub("", str(value).strip())

def strip_white_space(value):
    return str(value).strip()

def upper_case(value):
    return str(value).upper()

class StringLeft(object):
    
    def __init__(self, max_characters):
        self.max_characters = max_characters
        
    def __call__(self, value):
        if value:
            return str(value)[:self.max_characters]
        return value 