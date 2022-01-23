from src.utils import (get_combinations, get_ranges, convert_vector_to_address,
                       flat_range_addresses, convert_address_to_number,
                       convert_str_to_number)
from src.Errors import UncorrectSpreadsheetFileFormat, UncorrectSpreadsheetPath


def test_getting_combinations():
    alphabet = ['A', 'B', 'C']
    numbers = ['1', '2']
    comb = get_combinations(alphabet, numbers)
    assert comb == ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']


def test_getting_ranged_combinations():
    alphabet = get_ranges('A', 'D')
    numbers = ['2', '3', '4']
    comb = get_combinations(alphabet, numbers)
    assert comb == [
        'A2', 'A3', 'A4', 'B2', 'B3', 'B4', 'C2', 'C3', 'C4', 'D2', 'D3', 'D4'
        ]


def test_getting_flatted_address():
    adr = flat_range_addresses('E', 4, 'K', 5)
    assert adr == [
        'E4', 'E5', 'F4', 'F5', 'G4', 'G5', 'H4', 'H5',
        'I4', 'I5', 'J4', 'J5', 'K4', 'K5'
        ]
    adr = flat_range_addresses('A', 1, 'A', 2)
    assert adr == ['A1', 'A2']


def test_converting_address_to_number():
    tests = [
        (('A', 1), (1, 1)),
        (('O', 12), (15, 12)),
        (('X', 6), (24, 6)),
        (('AA', 2), (27, 2)),
        (('BA', 123), (53, 123)),
    ]
    for test in tests:
        vector = convert_address_to_number(*test[0])
        assert vector == test[1]


def test_converting_number_to_address():
    tests = [
        ((37466, 1), ('BCJZ', 1)),
        ((25, 1), ('Y', 1)),
        ((26, 1), ('Z', 1)),
        ((81, 1), ('CC', 1)),
        ((202, 1), ('GT', 1)),
        ((1, 1), ('A', 1)),
        ((37470, 1), ('BCKD', 1)),
    ]
    for test in tests:
        vector = convert_vector_to_address(*test[0])
        assert vector == test[1]


def test_converting_numer_to_address_complex():
    n = 100000
    for i in range(1, n+1):
        result = convert_address_to_number(*convert_vector_to_address(i, 1))
        assert result == (i, 1)


def test_converting_str_to_number_type():
    result = convert_str_to_number('123.0')
    assert isinstance(result, int)
    result = convert_str_to_number(str(34/17))
    assert isinstance(result, int)
    result = convert_str_to_number('123')
    assert isinstance(result, int)
    result = convert_str_to_number('123.34')
    assert isinstance(result, float)

