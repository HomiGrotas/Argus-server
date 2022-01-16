from random import randint, choices
from string import ascii_lowercase, hexdigits


def random_string(min_length=1, max_length=10):
    return ''.join(choices(ascii_lowercase, k=randint(min_length, max_length)))


def random_mac():
    mac_address = ''
    for i in range(6):
        mac_address += ':'+''.join(choices(hexdigits, k=2))
    return mac_address[1:]
