import random
import string

def generate_koupeans(count):
    """
    Generate a list of 'count' Koupean codes, each 12 characters long,
    consisting of uppercase letters and digits.
    """
    characters = string.ascii_uppercase + string.digits  # A-Z + 0-9
    koupeans = [''.join(random.choices(characters, k=12)) for _ in range(count)]
    return koupeans

