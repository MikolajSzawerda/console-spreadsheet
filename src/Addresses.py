import re
from src.Errors import UncorrectAddressAddressValue
from src.utils import (flat_range_addresses,
                       convert_address_to_number,
                       convert_vector_to_address)


class Address:
    def __init__(self, address: "str"):
        self._splitted_address = self._convert_to_xy(address)
        self._address = address
        if self._validate_address(address):
            self._x = str(self._splitted_address[0])
            self._y = str(self._splitted_address[1])

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

    def move(self, vector, max_dim, min_dim) -> "Address":
        adr_vector = convert_address_to_number(self.x, self.y)
        x_adr = adr_vector[0] + vector[0]
        y_adr = adr_vector[1] + vector[1]
        if x_adr <= min_dim[0]:
            x_adr = min_dim[0]
        if x_adr > max_dim[0]:
            x_adr = max_dim[0]
        if y_adr <= min_dim[1]:
            y_adr = min_dim[1]
        if y_adr > max_dim[1]:
            y_adr = max_dim[1]
        adr_text = convert_vector_to_address(x_adr, y_adr)
        return Address(''.join([str(x) for x in adr_text]))


class RangeAddress:
    def __init__(self, adrX: "Address" = None, adrY: "Address" = None):
        self._adrX = adrX
        self._adrY = adrY
        self._addresses = list()
        self._dimensions = self._get_dimensions()

    @property
    def addresses(self) -> 'list[Address]':
        if not self._addresses:
            self._generate_addresses()
        return self._addresses

    def get_absolute_coor(self):
        corner1 = convert_address_to_number(*self._adrX._splitted_address)
        corner2 = convert_address_to_number(*self._adrY._splitted_address)
        return (corner1, corner2)

    def _generate_addresses(self):
        addresses = flat_range_addresses(self._adrX.x, int(self._adrX.y),
                                         self._adrY.x, int(self._adrY.y))
        self._addresses = [Address(x) for x in addresses]

    @property
    def dimensions(self):
        return self._dimensions

    def _get_dimensions(self) -> 'tuple["int", "int"]':
        if self._adrX and self._adrY:
            a = convert_address_to_number(self._adrX.x, self._adrX.y)
            b = convert_address_to_number(self._adrY.x, self._adrY.y)
            return(abs(a[0]-b[0]) + 1, abs(a[1]-b[1]) + 1)
        else:
            return (0, 0)

    def split_addresses(self) -> 'tuple[list[str], list[str]]':
        adr = self.addresses
        xy_adrs = [x._splitted_address for x in adr]
        split_adr = list(zip(*xy_adrs))
        letters = sorted(set(split_adr[0]), key=lambda x: (len(x), x))
        numbers = [str(x) for x in sorted(set([int(x) for x in split_adr[1]]))]
        return (letters, numbers)

    @classmethod
    def from_address_list(cls: "RangeAddress",
                          addresses: "list[Address]") -> "RangeAddress":
        range_adr = cls()
        range_adr._addresses = addresses
        return range_adr
