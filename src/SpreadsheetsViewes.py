from src.Addresses import Address
from src.Spreadsheets import Spreadsheet
from src.Commands import CommandInterpreter
import curses
from time import sleep
from src.utils import convert_vector_to_address, convert_address_to_number
from config.spreadsheet_view_config import CELL_WIDTH, CELL_HEIGTH, ARROWS


class SpreadsheetView:
    def __init__(self, spreadsheet: "Spreadsheet"):
        self._spreadsheet = spreadsheet
        self._command_inter = CommandInterpreter(self.spreadsheet)

    @property
    def spreadsheet(self) -> "Spreadsheet":
        return self._spreadsheet

    def spreadsheet_view(self, stdscr: "curses._CursesWindow"):

        cursor = (1, 1)
        current_adr = Address('A1')
        dimmensions = self.spreadsheet.range.dimensions
        val = self.spreadsheet.cell(current_adr).value
        curses.noecho()
        curses.curs_set(0)
        stdscr.clear()
        target_address_win = curses.newwin(3, 8, 1, 1)
        command_terminal_win = curses.newwin(3, 128, 1, 8)
        command_terminal_win.keypad(1)
        rows = len(self.spreadsheet.range.addresses) + 2
        spreadsheet_cells_win = curses.newwin(rows, CELL_WIDTH, 4, 2)
        spreadsheet_cells_win.keypad(1)
        target_address_win.clear()
        command_terminal_win.clear()
        target_address_win.border()
        command_terminal_win.border()
        target_address_win.addstr(1, 1, f'{str(current_adr)}=')
        command_terminal_win.addstr(1, 1, f'{val}')
        target_address_win.refresh()
        command_terminal_win.refresh()
        while True:
            spreadsheet_cells_win.clear()
            pressed_key = spreadsheet_cells_win.get_wch()
            if pressed_key in ARROWS:
                vector = self._arrow_key_to_vector(pressed_key)
                new_adr = current_adr.move(vector, dimmensions)
                val = self.spreadsheet.cell(new_adr).value
                target_address_win.clear()
                command_terminal_win.clear()
                target_address_win.border()
                command_terminal_win.border()
                target_address_win.addstr(1, 1, f'{str(new_adr)}=')
                command_terminal_win.addstr(1, 1, f'{val}')
                target_address_win.refresh()
                command_terminal_win.refresh()
                current_adr = new_adr
        stdscr.refresh()

    def _arrow_key_to_vector(self, char):
        if char == ARROWS[0]:
            return (-1, 0)
        elif char == ARROWS[1]:
            return (0, -1)
        elif char == ARROWS[2]:
            return (1, 0)
        else:
            return (0, 1)
