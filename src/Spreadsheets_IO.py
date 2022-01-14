from distutils.fancy_getopt import wrap_text
from src.Spreadsheets import Spreadsheet
import csv
from src.Cells import Cell
from src.Addresses import RangeAddress, Address
from src.utils import convert_str_to_number


class SpreadsheetIO():
    def __init__(self, spreadsheet: 'Spreadsheet'):
        self._spreadsheet = spreadsheet

    def save_log(self):
        with open('log.txt', 'w') as fh:
            for line in self._spreadsheet.spreadsheet_view():
                line_to_write = ' '.join(line) + '\n'
                fh.write(line_to_write)

    def save_file(self):
        data = self._spreadsheet.spreadsheet_definition()
        try:
            with open(data[0], 'w') as fh:
                fh.write(f'{data[0]}\n')
                fh.write(f'{data[1]}\n')
                writer = csv.DictWriter(fh, [
                    'address', 'value', 'raw_value'
                ], delimiter=';')
                writer.writeheader()
                for row in data[2]:
                    writer.writerow({
                        'address': row[0],
                        'value': row[1],
                        'raw_value': row[2],
                    })
        except Exception:
            pass

    @staticmethod
    def load_spread_from_file(path: str) -> 'Spreadsheet':
        with open(path, 'r') as fh:
            loc = fh.readline().strip()
            adr = fh.readline()
            adrx, adry = adr.split(':')
            rangeAdr = RangeAddress(
                Address(adrx.strip()), Address(adry.strip())
            )
            reader = csv.DictReader(fh, delimiter=';')
            cells = list()
            for row in reader:
                try:
                    val = convert_str_to_number(row['value'])
                except Exception:
                    val = row['value']
                cell = Cell(Address(row['address']), val)
                cell._raw_data = row['raw_value']
                cells.append(cell)
            spread = Spreadsheet(rangeAdr, cells, localization=loc)
            return spread



