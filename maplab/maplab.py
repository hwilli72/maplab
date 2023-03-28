"""Main module."""

import string
import random

def random_string(length, upper=False, digits=False):
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    return ''.join(random.choice(letters) for i in range(length))
