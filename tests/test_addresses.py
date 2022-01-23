from src.Addresses import Address, RangeAddress
from src.Errors import UncorrectAddressAddressValue
import pytest


def test_creating_address():
    adr1 = Address('A1')
    assert adr1._address == 'A1'
    assert adr1._x == 'A'
    assert adr1._y == '1'
    assert str(adr1) == 'A1'


def test_spliting_address():
    assert Address._convert_to_xy('BBB234') == ("BBB", "234")
    assert Address._convert_to_xy('ABCDERFAS1') == ("ABCDERFAS", "1")
    assert Address._convert_to_xy('A12312321423423') == ("A", "12312321423423")


def test_wrong_addresses():
    with pytest.raises(UncorrectAddressAddressValue):
        Address('1A')

    with pytest.raises(UncorrectAddressAddressValue):
        Address('AAAA')

    with pytest.raises(UncorrectAddressAddressValue):
        Address('')

    with pytest.raises(UncorrectAddressAddressValue):
        Address('1234')


def test_creating_range_address():
    ra = RangeAddress(Address('A1'), Address('A2'))
    assert ra.addresses == [Address('A1'), Address('A2')]
    ra = RangeAddress(Address('A1'), Address('B2'))
    assert ra.addresses == [
        Address('A1'), Address('A2'), Address('B1'), Address('B2')
        ]


def test_creating_range_from_list():
    adr_list = [Address('A1'), Address('B3'), Address('C4')]
    range_adr = RangeAddress.from_address_list(adr_list)
    assert range_adr.addresses == adr_list


def test_range_dimmensions():
    tests = [
        (('A1', 'C3'), (3, 3)),
        (('E10', 'E14'), (1, 5)),
        (('L4', 'O12'), (4, 9)),
    ]
    for test in tests:
        adr = RangeAddress(Address(test[0][0]), Address(test[0][1]))
        assert adr.dimensions == test[1]


def test_moving_address_by_vector():
    range_adr = RangeAddress(Address('A1'), Address('C3'))
    tests = [
        (Address('B2'), (0, 0), Address('B2')),
        (Address('B2'), (1, 1), Address('C3')),
        (Address('C3'), (1, -1), Address('C2')),
        (Address('A1'), (-1, -1), Address('A1')),
        (Address('B1'), (10, 2), Address('C3')),
        (Address('C3'), (-2, -2), Address('A1')),
    ]
    for test in tests:
        move = test[0].move(test[1], range_adr.dimensions, (1, 1))
        assert move == test[2]


def test_range_addres_correctness():
    tests = [
        (Address('A1'), Address('B2'), True),
        (Address('A1'), Address('AAA1'), True),
        (Address('D3'), Address('D3'), True),
        (Address('B2'), Address('A1'), False),
        (Address('A1'), Address('A123'), True),
        (Address('A1'), Address('AA1'), True),
    ]
    for test in tests:
        pred = RangeAddress._check_range_adr_corners(test[0], test[1])
        assert pred is test[2]
