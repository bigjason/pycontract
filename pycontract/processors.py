import re

rm = re.compile("[^\d]")
def strip_non_numeric(value):
    return rm.sub("", str(value).strip())

def strip_white_space(value):
    return str(value).strip()

def upper_case(value):
    return str(value).upper()