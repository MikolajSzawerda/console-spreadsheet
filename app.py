from config.spreadsheet_view_config import SPREADSHEET
from src.SpreadsheetsViewes import SpreadsheetView
import curses
from curses import wrapper
from src.Spreadsheets_IO import SpreadsheetIO


def main():
    path = 'spreadsheet.csv'
    spr = SpreadsheetIO.load_spread_from_file(path)
    spr_view = SpreadsheetView(spr)
    wrapper(spr_view.spreadsheet_view)


if __name__ == '__main__':
    main()
