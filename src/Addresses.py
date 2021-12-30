import re
from src.Errors import UncorrectAddressAddressValue
from src.utils import flat_range_addresses, convert_address_to_number, convert_vector_to_address


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

    def move(self, vector, max_dim) -> "Address":
        adr_vector = convert_address_to_number(self.x, self.y)
        x_adr = adr_vector[0] + vector[0]
        y_adr = adr_vector[1] + vector[1]
        if x_adr <= 0:
            x_adr = 1
        if x_adr > max_dim[0]:
            x_adr = max_dim[0]
        if y_adr <= 0:
            y_adr = 1
        if y_adr > max_dim[1]:
            y_adr = max_dim[1]
        adr_text = convert_vector_to_address(x_adr, y_adr)
        return Address(''.join([str(x) for x in adr_text]))


class RangeAddress:
    def __init__(self, adrX: "Address" = None, adrY: "Address" = None):
        self._adrX = adrX
        self._adrY = adrY
        self._addresses = []
        self._dimensions = self._get_dimensions()
        if (adrX and adrY):
            addresses = flat_range_addresses(adrX.x, int(adrX.y),
                                             adrY.x, int(adrY.y))
            self._addresses = [Address(x) for x in addresses]

    @property
    def addresses(self) -> 'list[Address]':
        return self._addresses

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

    @classmethod
    def from_address_list(cls: "RangeAddress", addresses: "list[Address]") -> "RangeAddress":
        range_adr = cls()
        range_adr._addresses = addresses
        return range_adr
