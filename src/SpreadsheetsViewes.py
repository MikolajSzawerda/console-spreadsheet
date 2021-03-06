from src.Addresses import Address, RangeAddress
from src.Spreadsheets import Spreadsheet
from src.Commands import CommandInterpreter
from src.Spreadsheets_IO import SpreadsheetIO
import curses
from src.utils import convert_address_to_number, convert_vector_to_address
from config.spreadsheet_view_config import (CELL_WIDTH, CELL_HEIGTH,
                                            ARROWS, TABLE_COOR, VIEW_SIZE)
import sys


class SpreadsheetView:
    def __init__(self, spreadsheet: "Spreadsheet"):
        self._spreadsheet = spreadsheet
        self._command_inter = CommandInterpreter(self.spreadsheet)
        self._spread_io = SpreadsheetIO(self.spreadsheet)
        self._saved = True
        self._view_range = VIEW_SIZE
        self._current_adr = self._view_range._adrX
        self._view_dimmensions = self._view_range.dimensions
        self._spread_view = self._view_range.get_absolute_coor()

    @property
    def spreadsheet(self) -> "Spreadsheet":
        return self._spreadsheet

    @property
    def view_range(self) -> "RangeAddress":
        return self._view_range

    @property
    def saved(self) -> bool:
        return self._saved

    @saved.setter
    def saved(self, val):
        self._saved = val
        self._draw_save_bar(val)

    def _init_view(self, stdscr: "curses._CursesWindow"):
        '''
        Init all curses windows, determines spreadhseet size,
        and draws everything
        '''
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.clear()
        stdscr.refresh()
        curses.noecho()
        curses.curs_set(0)
        self._table_x = (self._view_dimmensions[0] + 1) * (CELL_WIDTH) + 2
        self._table_y = (self._view_dimmensions[1] + 1) * CELL_HEIGTH + 2
        self._spreadsheet_cells_win = curses.newpad(self._table_y,
                                                    self._table_x)
        self._save_win = curses.newwin(1, self._table_x, 1, 1)
        self._target_address_win = curses.newwin(3, 8, 2, 1)
        self._command_terminal_win = curses.newwin(3, self._table_x-7, 2, 8)
        self._top_bar = (self._target_address_win, self._command_terminal_win)
        self._command_terminal_win.keypad(1)
        self._spreadsheet_cells_win.keypad(1)
        val = self.spreadsheet.cell(self._current_adr).value
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(self._current_adr)}')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._draw_table()
        self._refresh(self._top_bar)
        self._draw_save_bar(self.saved)

    def _draw_save_bar(self, saved: bool):
        '''
        Draw save bar with file localization
        '''
        star = '' if saved else '*'
        msg = star+self._spreadsheet._localization
        size = self._table_x-2
        bar = f'{msg:^{size}}'
        self._save_win.attron(curses.color_pair(4))
        self._save_win.addstr(0, 1, bar)
        self._save_win.attroff(curses.color_pair(4))
        self._save_win.refresh()

    def spreadsheet_view(self, stdscr: "curses._CursesWindow"):
        '''
        Function handles all input from user
        '''
        self._screen = stdscr
        self._init_view(stdscr)
        self._set_max_spread_view()
        self._draw_cell(self._current_adr, curses.color_pair(4))
        self._refresh_table()
        self._draw_save_bar(True)
        while True:
            pressed_key = self._spreadsheet_cells_win.get_wch()
            if pressed_key in ARROWS:
                self._cursor_movement(pressed_key)
            if pressed_key == 'i':
                self._edit_mode()
                self.saved = False
            if pressed_key == 's':
                self._spread_io.save_file()
                self.saved = True
            if pressed_key == 'q':
                sys.exit(0)
            if pressed_key == 410:
                self._set_max_spread_view()

    def _set_max_spread_view(self):
        '''
        Function set spreadsheet size to fit terminal size
        '''
        x, y = self._get_max_dimmensions()
        corner = self._view_range._adrX
        max_adr = corner.move((x-1, y-1),
                              self.spreadsheet.range.dimensions, (1, 1))
        rang = RangeAddress(corner, max_adr)
        self._set_view_range(rang)
        self._current_adr = self._view_range._adrX

    def _get_max_dimmensions(self):
        '''
        Function determines max spreadsheet size
        '''
        y, x = self._screen.getmaxyx()
        max_y = abs(int((y-8)/CELL_HEIGTH))
        max_x = abs(int((x-10)/CELL_WIDTH)-1)
        return max_x, max_y

    def _set_view_range(self, range_adr: "RangeAddress"):
        '''
        Function updates all vars when changing spreadsheet size
        '''
        self._view_range = range_adr
        self._view_dimmensions = self._view_range.dimensions
        self._spread_view = self._view_range.get_absolute_coor()
        self._init_view(self._screen)

    def _arrow_key_to_vector(self, char):
        '''
        Function converts arrow input to vector
        '''
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
        '''
        Function draws current cursor cell, redraw old one,
        and if needed invokes change of view range
        '''
        vector = self._arrow_key_to_vector(arrow_key)
        self._draw_cell(self._current_adr, curses.color_pair(0))
        new_adr = self._transform_adr(self._current_adr, vector)
        self._draw_cell(new_adr, curses.color_pair(4))
        val = self.spreadsheet.cell(new_adr)._raw_data
        self._clear(self._top_bar)
        self._border(self._top_bar)
        self._target_address_win.addstr(1, 1, f'{str(new_adr)}')
        self._command_terminal_win.addstr(1, 1, f'{val}')
        self._refresh(self._top_bar)
        self._current_adr = new_adr
        self._refresh_table()

    def _edit_mode(self):
        '''
        Function for editing cell value
        '''
        val = self.spreadsheet.cell(self._current_adr)._raw_data
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
        self._draw_table()
        return

    def _refresh_table(self):
        y = self._table_y + TABLE_COOR[0]
        x = self._table_x + TABLE_COOR[1]
        self._spreadsheet_cells_win.refresh(0, 0, *TABLE_COOR, y, x)

    def _draw_table(self):
        table = self._spreadsheet_cells_win
        table.border()
        self._draw_labels()
        addrs = self._view_range.addresses
        for adr in addrs:
            self._draw_cell(adr)
        self._draw_cell(self._current_adr, curses.color_pair(4))
        self._refresh_table()

    def _draw_labels(self):
        '''
        Function draws rows and columns labels like in excel
        '''
        table = self._spreadsheet_cells_win
        letters, numbers = self._view_range.split_addresses()
        letters.insert(0, '')
        for k, i in enumerate(range(1, self._table_x-1, CELL_WIDTH)):
            cell = f'{letters[k]:^{CELL_WIDTH}}'
            table.attron(curses.color_pair(3))
            table.attron(curses.A_BOLD)
            table.addstr(1, i, cell)
            table.attroff(curses.A_BOLD)
            table.attroff(curses.color_pair(3))
        for i in range(1, self._table_y-2):
            cell = f'{numbers[i-1]:^{CELL_WIDTH}}'
            table.attron(curses.color_pair(3))
            table.attron(curses.A_BOLD)
            table.addstr(i+1, 1, cell)
            table.attroff(curses.A_BOLD)
            table.attroff(curses.color_pair(3))

    def _draw_cell(self, adress: "Address", color=None):
        '''
        Function redraw cell at given address including different view range
        '''
        cell = self.spreadsheet.cell(adress)
        val = cell.value if cell._raw_data else cell._raw_data
        formatted_cell = f'|{val:^{CELL_WIDTH-2}}|'
        offset_adr = adress.move([-(x-1) for x in self._spread_view[0]],
                                 self._view_dimmensions, (1, 1))
        num = convert_address_to_number(offset_adr.x, offset_adr.y)
        y = num[1] + 1
        x = num[0] * CELL_WIDTH + 1
        if color:
            self._spreadsheet_cells_win.attron(color)
            self._spreadsheet_cells_win.attron(curses.A_BOLD)
        self._spreadsheet_cells_win.addstr(y, x, formatted_cell)
        if color:
            self._spreadsheet_cells_win.attroff(curses.A_BOLD)
            self._spreadsheet_cells_win.attroff(color)

    def _transform_adr(self, adr: "Address", vector) -> "Address":
        '''
        Function handles address movement by vector including spreadsheet size
        and current view range if needed function invokes change of view range
        '''
        adr_vector = convert_address_to_number(adr.x, adr.y)
        max_dim = self._spread_view[1]
        min_dim = self._spread_view[0]
        x_adr = adr_vector[0] + vector[0]
        y_adr = adr_vector[1] + vector[1]
        transform_vect = (0, 0)

        if x_adr < min_dim[0]:
            x_adr = min_dim[0]
            transform_vect = (-1, transform_vect[1])
        if x_adr > max_dim[0]:
            x_adr = max_dim[0]
            transform_vect = (1, transform_vect[1])
        if y_adr < min_dim[1]:
            y_adr = min_dim[1]
            transform_vect = (transform_vect[0], -1)
        if y_adr > max_dim[1]:
            y_adr = max_dim[1]
            transform_vect = (transform_vect[0], 1)
        self._move_spread_view(transform_vect)
        adr_text = convert_vector_to_address(x_adr, y_adr)
        return Address(''.join([str(x) for x in adr_text]))

    def _move_spread_view(self, transform_vector):
        '''
        Function moves current view range by given vector
        '''
        dim = self.spreadsheet.range.dimensions
        x_range = self._view_range._adrX.move(transform_vector, dim, (1, 1))
        y_range = self._view_range._adrY.move(transform_vector, dim, (1, 1))
        new_range = RangeAddress(x_range, y_range)
        len_predict = (new_range.dimensions == self._view_range.dimensions)
        vect_predict = any(x != 0 for x in transform_vector)
        if len_predict and vect_predict:
            self._set_view_range(RangeAddress(x_range, y_range))
