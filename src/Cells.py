from Addresses import Address


class Cell:
    def __init__(self, address: "Address", value):
        self._address = address
        self._value = value

    @property
    def address(self) -> "Address":
        return self._address

    @property
    def value(self) -> "str":
        return self._value

    @value.setter
    def value(self, val: "str"):
        self._value = val
