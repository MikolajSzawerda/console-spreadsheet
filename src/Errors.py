class UncorrectAddressAddressValue(Exception):
    def __init__(self, address: str) -> None:
        msg = f'{address} nie jest poprawnym adresem!'
        super().__init__(msg)


class CellNotInSpreadsheetError(Exception):
    def __init__(self, address: "str") -> None:
        msg = f'Komórki o adresie{address} nie ma w arkuszu!'
        super().__init__(msg)
