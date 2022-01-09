from src.Addresses import Address
from src.Spreadsheets import Spreadsheet
from src.Commands import CommandInterpreter
import curses
from src.utils import get_ranges, convert_address_to_number
from config.spreadsheet_view_config import CELL_WIDTH, CELL_HEIGTH, ARROWS, TABLE_COOR


class SpreadsheetView:
    def __init__(self, spreadsheet: "Spreadsheet"):
        self._spreadsheet = spreadsheet
        self._command_inter = CommandInterpreter(self.spreadsheet)
        self._current_adr = Address('A1')
        self._dimmensions = self.spreadsheet.range.dimensions

    @property
    def spreadsheet(self) -> "Spreadsheet":
        return self._spreadsheet

    def _init_view(self, stdscr: "curses._CursesWindow"):
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.clear()
        curses.noecho()
        curses.curs_set(0)
        self._table_x = (self._dimmensions[0] + 1) * (CELL_WIDTH) + 2
        self._table_y = (self._dimmensions[1] + 1) * CELL_HEIGTH + 2
        self._spreadsheet_cells_win = curses.newpad(self._table_y, self._table_x)
        self._target_address_win = curses.newwin(3, 8, 1, 1)
        self._command_terminal_win = curses.newwin(3, self._table_x-7, 1, 8)
        self._top_bar = (self._target_address_win, self._command_terminal_win)
        self._command_terminal_win.keypad(1)
        self._spreadsheet_cells_win.keypad(1)
        val = self.spreadsheet.cell(self._current_adr).value
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(self._current_adr)}=')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._draw_table()
        self._refresh(self._top_bar)

    def spreadsheet_view(self, stdscr: "curses._CursesWindow"):
        self._init_view(stdscr)
        while True:
            # self._spreadsheet_cells_win.clear()
            pressed_key = self._spreadsheet_cells_win.get_wch()
            if pressed_key in ARROWS:
                self._cursor_movement(pressed_key)
            if pressed_key == 'i':
                self._edit_mode()
            # self._draw_table()
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
        self._draw_cell(self._current_adr)
        new_adr = self._current_adr.move(vector, self._dimmensions)
        self._draw_cell(new_adr, curses.color_pair(4))
        val = self.spreadsheet.cell(new_adr)._raw_data
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(new_adr)}=')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._refresh(self._top_bar)
        self._current_adr = new_adr
        self._refresh_table()

    def _edit_mode(self):
        val = self.spreadsheet.cell(self._current_adr).value
        ctw = self._command_terminal_win
        line = str(val)
        self._border([ctw], curses.color_pair(1))
        self._refresh([ctw])
        while True:
            key = self._command_terminal_win.get_wch()
            if key == '\n':
                self._border([ctw], curses.color_pair(2))
                self._refresh([ctw])
                break
            elif key == 263:
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

    def _refresh_table(self):
        y = self._table_y + TABLE_COOR[0]
        x = self._table_x + TABLE_COOR[1]
        self._spreadsheet_cells_win.refresh(0, 0, *TABLE_COOR, y, x)

    def _draw_table(self):
        table = self._spreadsheet_cells_win
        table.border()
        for i in range(2, self._table_y-1):
            for j in range(CELL_WIDTH+1, self._table_x-1, CELL_WIDTH):
                table.addstr(i, j, f'|{"hui":^{CELL_WIDTH-2}}|')
        self._draw_labels()
        addrs = self.spreadsheet.range.addresses
        for adr in addrs:
            self._draw_cell(adr)
        self._draw_cell(self._current_adr, curses.color_pair(4))
        self._refresh_table()

    def _draw_labels(self):
        table = self._spreadsheet_cells_win
        max_letter = self.spreadsheet.range._adrY.x
        bar = get_ranges('A', max_letter)
        bar.insert(0, '')
        for k, i in enumerate(range(1, self._table_x-1, CELL_WIDTH)):
            cell = f'{bar[k]:^{CELL_WIDTH}}'
            table.attron(curses.color_pair(3))
            table.attron(curses.A_BOLD)
            table.addstr(1, i, cell)
            table.attroff(curses.A_BOLD)
            table.attroff(curses.color_pair(3))
        for i in range(1, self._table_y-2):
            cell = f'{i:^{CELL_WIDTH}}'
            table.attron(curses.color_pair(3))
            table.attron(curses.A_BOLD)
            table.addstr(i+1, 1, cell)
            table.attroff(curses.A_BOLD)
            table.attroff(curses.color_pair(3))

    def _draw_cell(self, adress: "Address", color=None):
        val = self.spreadsheet.cell(adress).value
        cutted_val = str(val).replace('"', '')[:CELL_WIDTH-2]
        cell = f'|{cutted_val:^{CELL_WIDTH-2}}|'
        num = convert_address_to_number(adress.x, adress.y)
        y = num[1] + 1
        x = num[0] * CELL_WIDTH + 1
        if color:
            self._spreadsheet_cells_win.attron(color)
            self._spreadsheet_cells_win.attron(curses.A_BOLD)
        self._spreadsheet_cells_win.addstr(y, x, cell)
        if color:
            self._spreadsheet_cells_win.attroff(curses.A_BOLD)
            self._spreadsheet_cells_win.attroff(color)
