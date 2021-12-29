import re
from src.Errors import UncorrectAddressAddressValue
from src.utils import flat_range_addresses


class Address:
    def __init__(self, address: "str"):
        splitted_address = self._convert_to_xy(address)
        self._address = address
        if self._validate_address(address):
            self._x = str(splitted_address[0])
            self._y = str(splitted_address[1])

    @property
    def x(self) -> "str":
        return self._x

    @property
    def y(self) -> "str":
        return self._y

    def __str__(self) -> "str":
        return self._address

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: "Address"):
        return (self._address == other._address)

    @staticmethod
    def _convert_to_xy(address: "str") -> "tuple[str, str]":
        splitted_address = re.split("(\d+)", address)
        return tuple(filter(None, splitted_address))

    def _validate_address(self, address: "str"):
        val = self._convert_to_xy(address)
        if len(val) != 2:
            raise UncorrectAddressAddressValue(address)
        if not (val[0].isalnum() and val[1].isdigit()):
            raise UncorrectAddressAddressValue(address)
        return True


class RangeAddress:
    def __init__(self, adrX: "Address" = None, adrY: "Address" = None):
        self._adrX = adrX
        self._adrY = adrY
        self._addresses = []
        if (adrX and adrY):
            addresses = flat_range_addresses(adrX.x, int(adrX.y),
                                             adrY.x, int(adrY.y))
            self._addresses = [Address(x) for x in addresses]

    @property
    def addresses(self) -> 'list[Address]':
        return self._addresses

    @classmethod
    def from_address_list(cls: "RangeAddress", addresses: "list[Address]") -> "RangeAddress":
        range_adr = cls()
        range_adr._addresses = addresses
        return range_adr
