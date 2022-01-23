from src.Spreadsheets import Spreadsheet
from config.spreadsheet_view_config import SPREADSHEET
from src.SpreadsheetsViewes import SpreadsheetView
from curses import wrapper
from src.Spreadsheets_IO import SpreadsheetIO
import sys
import argparse


def arguments_handler(args, parser: 'argparse.ArgumentParser') -> Spreadsheet:
    argv = parser.parse_args(args[1:])
    if argv.load_spreadsheet:
        path = argv.load_spreadsheet
        return SpreadsheetIO.load_spread_from_file(path)
    elif argv.new_spreadsheet:
        localization = argv.new_spreadsheet[0]
        size = argv.new_spreadsheet[1]
        return SpreadsheetIO.create_file(localization, size)
    else:
        return SPREADSHEET


def main(args):
    parser = argparse.ArgumentParser()
    help = [
        'Open spreadsheet at given localization',
        'Create new spreadsheet at given localization and given size'
        ]
    files_group = parser.add_mutually_exclusive_group()
    files_group.add_argument('-l', '--load_spreadsheet',
                             help=help[0], metavar='localization')
    files_group.add_argument('-n', '--new_spreadsheet', nargs=2, help=help[1],
                             metavar=('localization', 'size'))
    spr = arguments_handler(args, parser)
    spr = spr if spr else SPREADSHEET
    spr_view = SpreadsheetView(spr)
    wrapper(spr_view.spreadsheet_view)


if __name__ == '__main__':
    main(sys.argv)
