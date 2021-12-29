from src.Addresses import Address


class Cell:
    def __init__(self, address: "Address", value: "str" = None):
        self._address = address
        self._value = value if value else 0
        self._raw_data = str(self._value)

    @property
    def address(self) -> "Address":
        return self._address

    @property
    def value(self) -> "str":
        return self._value

    @value.setter
    def value(self, val: "str"):
        self._value = val

    def __eq__(self, other: "Cell") -> bool:
        return (self.address == other.address)
