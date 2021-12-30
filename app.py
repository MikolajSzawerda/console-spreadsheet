from config.spreadsheet_view_config import SPREADSHEET
from src.SpreadsheetsViewes import SpreadsheetView
import curses
from curses import wrapper


def main():
    spr = SPREADSHEET
    spr_view = SpreadsheetView(spr)
    wrapper(spr_view.spreadsheet_view)


if __name__ == '__main__':
    main()
