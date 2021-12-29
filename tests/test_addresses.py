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
