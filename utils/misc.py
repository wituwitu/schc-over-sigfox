"""Module of miscellaneous functions used in the project."""
import os


def zfill(string: str, length: int) -> str:
    """Adds zeroes at the begginning of a string until it completes
    the desired length."""
    return '0' * (length - len(string)) + string


def replace_char(string: str, position: int, new_char: str) -> str:
    """Replaces a single character in the specified position of a string."""
    return f"{string[:position]}{new_char}{string[position + 1:]}"


def is_monochar(string: str, char: str = None) -> bool:
    """Checks if a string contains only repetitions of one character."""
    monochar = len(set(string)) == 1

    if char is not None:
        return monochar and string[0] == char

    return monochar


def generate_packet(byte_size: int, path: str = None) -> bytes:
    """Generates a string of the specified byte size and
    optionally saves it into a file."""

    string = '0'
    i = 0
    while len(string) < byte_size:
        i = (i + 1) % 10
        string += str(i)

    string = string.encode('utf-8')

    if path is not None and not os.path.isfile(path):
        with open(path, 'wb') as fil:
            fil.write(string)

    return string


def round_to_next_multiple(num, factor):
    """Rounds a number to the next greater multiple of a specified factor."""
    return -(num // (-factor)) * factor
