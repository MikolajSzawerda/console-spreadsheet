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
        self._current_adr = Address('A1')

    @property
    def spreadsheet(self) -> "Spreadsheet":
        return self._spreadsheet

    def _init_view(self, stdscr: "curses._CursesWindow"):
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.clear()
        curses.noecho()
        curses.curs_set(0)
        self._target_address_win = curses.newwin(3, 8, 1, 1)
        self._command_terminal_win = curses.newwin(3, 128, 1, 8)
        self._top_bar = (self._target_address_win, self._command_terminal_win)
        rows = len(self.spreadsheet.range.addresses) + 2
        self._spreadsheet_cells_win = curses.newwin(rows, CELL_WIDTH, 4, 2)
        self._command_terminal_win.keypad(1)
        self._spreadsheet_cells_win.keypad(1)
        val = self.spreadsheet.cell(self._current_adr).value
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(self._current_adr)}=')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._refresh(self._top_bar)

    def spreadsheet_view(self, stdscr: "curses._CursesWindow"):
        self._dimmensions = self.spreadsheet.range.dimensions
        self._init_view(stdscr)
        while True:
            self._spreadsheet_cells_win.clear()
            pressed_key = self._spreadsheet_cells_win.get_wch()
            if pressed_key in ARROWS:
                self._cursor_movement(pressed_key)
            if pressed_key == 'i':
                self._edit_mode()
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

    def _clear(self, windows: "list[curses._CursesWindow]"):
        for window in windows:
            window.clear()

    def _refresh(self, windows: "list[curses._CursesWindow]"):
        for window in windows:
            window.refresh()

    def _border(self, windows: "list[curses._CursesWindow]", color=None):
        for window in windows:
            if color:
                window.attron(color)
            window.border()
            if color:
                window.attroff(color)

    def _cursor_movement(self, arrow_key):
        vector = self._arrow_key_to_vector(arrow_key)
        new_adr = self._current_adr.move(vector, self._dimmensions)
        val = self.spreadsheet.cell(new_adr).value
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(new_adr)}=')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._refresh(self._top_bar)
        self._current_adr = new_adr

    def _edit_mode(self):
        val = self.spreadsheet.cell(self._current_adr).value
        ctw = self._command_terminal_win
        line = str(val)
        self._border([ctw], curses.color_pair(1))
        self._refresh([ctw])
        while True:
            key = self._command_terminal_win.getkey()
            if key == '\n':
                self._border([ctw], curses.color_pair(2))
                self._refresh([ctw])
                break
            if key == 'KEY_BACKSPACE':
                line = line[:-1]
            else:
                line += key
            self._clear([ctw])
            self._border([ctw], curses.color_pair(1))
            ctw.attron(curses.A_BOLD)
            ctw.addstr(1, 1, f'{line}')
            ctw.attroff(curses.A_BOLD)
            self._refresh([ctw])
        cmd = f'{self._current_adr}={line}'
        self._command_inter.parse_command(cmd)
        return
