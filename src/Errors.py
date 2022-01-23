class UncorrectAddressAddressValue(Exception):
    '''
    Given address text is not correct address
    '''
    def __init__(self, address: str) -> None:
        msg = f'{address} nie jest poprawnym adresem!'
        super().__init__(msg)


class UncorrectRangeAddressBounds(Exception):
    '''
    Given range address corners are not correct
    '''
    def __init__(self, address: str) -> None:
        msg = f'{address} nie jest poprawnym zakresm adresów!'
        super().__init__(msg)


class CellNotInSpreadsheetError(Exception):
    def __init__(self, address: "str") -> None:
        msg = f'Komórki o adresie{address} nie ma w arkuszu!'
        super().__init__(msg)


class NoTargetCommandAddressError(Exception):
    '''
    Given command doesn't contain target cell
    '''
    def __init__(self, cmd: "str") -> None:
        msg = f'Komenda {cmd} nie ma podanej komórki docelowej!'
        super().__init__(msg)


class UncorrectSpreadsheetPath(Exception):
    '''
    Path does not lead to spreadsheet gile
    '''
    def __init__(self, path: str) -> None:
        msg = f'{path} nie jest poprawną ścieżką do pliku arkusza'
        super().__init__(msg)


class UncorrectSpreadsheetFileFormat(Exception):
    '''
    Given file is not a spreadsheet file
    '''
    def __init__(self, file_name: str) -> None:
        msg = f'{file_name} nie jest prawidłowym plikiem arkusza'
        super().__init__(msg)


class MalformedSpreadsheetFile(Exception):
    '''
    Spreadsheet file cannot be read correctly
    '''
    def __init__(self, file_name: str) -> None:
        msg = f'{file_name} jest uszkodzony!'
        super().__init__(msg)


class UncorrectSpreadsheetSize(Exception):
    '''
    Given spreadsheet size is not correct
    '''
    def __init__(self, size: str) -> None:
        msg = f'{size} nie jest prawidłowym wymiarem arkusza(format Number:Number)'
        super().__init__(msg)


class UncorrectCommand(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UncorrectCommandName(UncorrectCommand):
    '''
    Spreadsheet doesn't support given command, or command is misspeld
    '''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UncorrectGivenCommandValues(UncorrectCommand):
    '''
    Given command parametrs aren't correct
    '''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RecursiveCommands(UncorrectCommand):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
