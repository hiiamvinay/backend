import random
import string

def random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=8))
    return password