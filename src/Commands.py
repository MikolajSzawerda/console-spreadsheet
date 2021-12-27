from src.Addresses import Address
from src.Spreadsheets import Spreadsheet
from config.commands_config import commands


class Command():
    def __init__(self, cmd, range):
        self._func = commands[cmd]
        self._range = range

    def execute(self):
        response = self._func(self._range)
        return response


class Task():
    def __init__(self, address: "Address", command=None):
        self._address = address
        self._command = command

    def execute(self, spreadsheet: "Spreadsheet", val=None):
        if (val is None) and (self._command is None):
            return spreadsheet.cell(self._address).value
        else:
            spreadsheet.set_cell_val(self._address, val)
            return True


class CommandInterpreter():
    def __init__(self, spreadsheet: "Spreadsheet"):
        self._spreadsheet = spreadsheet

    @property
    def spreadsheet(self):
        return self._spreadsheet

    def _shell_values(self, cmd: "str"):
        words = cmd.split('=')
        address, value = (None, None)
        try:
            address = Address(words[0])
        except IndexError:
            pass
        try:
            value = words[1]
        except IndexError:
            pass
        return [tuple([address]), value]

    def parse_command(self, cmd: "str"):
        words = self._shell_values(cmd)
        com = Task(*words[0])
        response = com.execute(self.spreadsheet, words[1])
        return response
