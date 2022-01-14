from string import ascii_uppercase
import itertools
import os
from src.Errors import (UncorrectSpreadsheetPath,
                        UncorrectSpreadsheetFileFormat,
                        UncorrectSpreadsheetSize)
import re


def _letter_iter():
    for num in itertools.count(1):
        for letter in itertools.product(ascii_uppercase, repeat=num):
            yield ''.join(letter)


def get_ranges(alA, alB):
    '''
    Function returns excels-like columns label in alA, alB borders
    '''
    if alA == alB:
        return [alA]
    letters = []
    rang = _letter_iter()
    for letter in rang:
        if letter == alA:
            letters.append(letter)
            break
    for letter in rang:
        letters.append(letter)
        if letter == alB:
            break
    return letters


def get_combinations(alphabet, numbers):
    '''
    Function creates combinations of given arrs
    '''
    return [''.join(pair) for pair in itertools.product(alphabet, numbers)]


def flat_range_addresses(alA, nrA, alB, nrB):
    '''
    Function create list of excel-like addresses
    '''
    letters = get_ranges(alA, alB)
    numbers = [str(x) for x in range(nrA, nrB+1)]
    return get_combinations(letters, numbers)


def convert_address_to_number(letters: "str", number: "str"):
    letters_to_num = 0
    for letter in letters:
        letters_to_num = letters_to_num * 26 + (ord(letter) - 65) +1
    return (letters_to_num, int(number))


def convert_vector_to_address(adr_x: "int", adr_y: "int"):
    letter = ''
    while adr_x // 26:
        if adr_x == 26:
            break
        letter_num = adr_x % 26
        if not letter_num:
            letter = 'Z' + letter
            adr_x = (adr_x // 26) - 1
            continue
        else:
            letter = chr(letter_num + 64) + letter
        adr_x = adr_x // 26
    if adr_x == 26:
        letter = 'Z' + letter
    else:
        letter = chr(adr_x % 26 + 64) + letter
    return (letter, adr_y)


def convert_str_to_number(text_number: "str"):
    '''
    Function converts string number for the most suitble data type
    '''
    number = 0
    if '.' in text_number:
        mantisa = text_number.split('.')[1]
        if int(mantisa) == 0:
            number = int(text_number)
        else:
            number = float(text_number)
    else:
        number = int(text_number)
    return number


def check_file(path: "str", to_read: bool = False):
    if to_read:
        if not os.path.isfile(path):
            raise UncorrectSpreadsheetPath(path)
    if not path.endswith('.csv'):
        raise UncorrectSpreadsheetFileFormat(os.path.basename(path))
    return True


def convert_to_range(size: "str"):
    try:
        x, y = re.split('[:,x,,|]', size)
        x, y = int(x), int(y)
        if (x <= 0) or (y <= 0):
            raise UncorrectSpreadsheetSize(size)
        return [str(x) for x in convert_vector_to_address(x, y)]
    except Exception as e:
        raise UncorrectSpreadsheetSize(size) from e
