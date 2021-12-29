from string import ascii_uppercase
import itertools


def _letter_iter():
    for num in itertools.count(1):
        for letter in itertools.product(ascii_uppercase, repeat=num):
            yield ''.join(letter)


def get_ranges(alA, alB):
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
    return [''.join(pair) for pair in itertools.product(alphabet, numbers)]


def flat_range_addresses(alA, nrA, alB, nrB):
    letters = get_ranges(alA, alB)
    numbers = [str(x) for x in range(nrA, nrB+1)]
    return get_combinations(letters, numbers)
