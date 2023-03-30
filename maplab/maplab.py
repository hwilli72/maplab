"""Main module."""

import string
import random
import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, center, zoom, **kwargs) -> None:
        super().__init__(center=center, zoom=zoom, **kwargs)

def random_string(length, upper=False, digits=False):
    """Generates a random string of a given length.

    Args:
        length (_type_): The length of the string to generate.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.

    Returns:
        str: random string
    """    
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    return ''.join(random.choice(letters) for i in range(length))
