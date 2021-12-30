from string import ascii_uppercase
import itertools


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
