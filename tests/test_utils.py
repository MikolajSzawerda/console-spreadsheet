from src.utils import get_combinations, get_ranges, flat_range_addresses


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
