from src.Addresses import Address


class Cell:
    def __init__(self, address: "Address", value: "str" = None):
        self._address = address
        self._value = value if value else 0

    @property
    def address(self) -> "Address":
        return self._address

    @property
    def value(self) -> "str":
        return self._value

    @value.setter
    def value(self, val: "str"):
        self._value = val
