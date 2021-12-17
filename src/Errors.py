class UncorrectAddressAddressValue(Exception):
    def __init__(self, address: str) -> None:
        msg = f'{address} nie jest poprawnym adresem!'
        super().__init__(msg)
