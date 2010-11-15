
NUMBER_CHARACTERS = {str(x) for x in range(10)}
def strip_non_numeric(value_in):
    result = []
    for c in str(value_in).strip():
        if c in NUMBER_CHARACTERS:
            result.append(c)
    return "".join(result)

def strip_white_space(value):
    return value.strip()
