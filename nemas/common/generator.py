import random
import string


def generate_alphanumeric_code(length=6):
    characters = string.ascii_uppercase + string.digits  # A-Z and 0-9
    return "".join(random.choices(characters, k=length))


def generate_numeric_code(length=5):
    characters = string.digits  # 0-9
    return "".join(random.choices(characters, k=length))
