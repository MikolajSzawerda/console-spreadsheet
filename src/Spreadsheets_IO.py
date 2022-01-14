import os
import csv
from src.Spreadsheets import Spreadsheet
from src.Cells import Cell
from src.Addresses import RangeAddress, Address
from src.utils import convert_str_to_number
from src.utils import check_file, convert_to_range
from src.Errors import MalformedSpreadsheetFile


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
        if check_file(data[0]):
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

    @staticmethod
    def load_spread_from_file(path: str) -> 'Spreadsheet':
        if check_file(path, True):
            with open(path, 'r') as fh:
                try:
                    loc = fh.readline().strip()
                    check_file(loc)
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
                except Exception:
                    raise MalformedSpreadsheetFile(os.path.basename(path))
                return spread

    @staticmethod
    def create_file(path: str, size: str) -> 'Spreadsheet':
        check_file(path)
        adrY = Address(''.join(convert_to_range(size)))
        adrX = Address('A1')
        range_adr = RangeAddress(adrX, adrY)
        spr = Spreadsheet(range_adr, localization=path)
        SpreadsheetIO(spr).save_file()
        return spr
