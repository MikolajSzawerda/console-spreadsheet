from mimetypes import init


class UncorrectAddressAddressValue(Exception):
    def __init__(self, address: str) -> None:
        msg = f'{address} nie jest poprawnym adresem!'
        super().__init__(msg)


class CellNotInSpreadsheetError(Exception):
    def __init__(self, address: "str") -> None:
        msg = f'Komórki o adresie{address} nie ma w arkuszu!'
        super().__init__(msg)


class NoTargetCommandAddressError(Exception):
    def __init__(self, cmd: "str") -> None:
        msg = f'Komenda {cmd} nie ma podanej komórki docelowej!'
        super().__init__(msg)


class UncorrectSpreadsheetPath(Exception):
    def __init__(self, path: str) -> None:
        msg = f'{path} nie jest poprawną ścieżką do pliku arkusza'
        super().__init__(msg)


class UncorrectSpreadsheetFileFormat(Exception):
    def __init__(self, file_name: str) -> None:
        msg = f'{file_name} nie jest prawidłowym plikiem arkusza'
        super().__init__(msg)


class MalformedSpreadsheetFile(Exception):
    def __init__(self, file_name: str) -> None:
        msg = f'{file_name} jest uszkodzony!'
        super().__init__(msg)


class UncorrectSpreadsheetSize(Exception):
    def __init__(self, size: str) -> None:
        msg = f'{size} nie jest prawidłowym wymiarem arkusza(format Number:Number)'
        super().__init__(msg)


class UncorrectCommand(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UncorrectCommandName(UncorrectCommand):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UncorrectGivenCommandValues(UncorrectCommand):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
