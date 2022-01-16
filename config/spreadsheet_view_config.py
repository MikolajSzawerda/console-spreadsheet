from src.Addresses import Address, RangeAddress
from src.Cells import Cell
from src.Spreadsheets import Spreadsheet

adr1 = 'A1'
adr2 = 'AAAAAAAAAAAAAAAAAA1000000000000000000000'


SPREADSHEET = Spreadsheet(RangeAddress(Address(adr1), Address(adr2)), [
    Cell(Address('A1'), 2),
    Cell(Address('A2'), -5),
    Cell(Address('A3')),
    Cell(Address('B1'), '"Hello world"'),
    Cell(Address('B2'), 12),
    Cell(Address('B3'), 120),
    Cell(Address('C1'), 0),
    Cell(Address('C2'), 1),
    Cell(Address('C3'), 69),
], localization='spreadsheet.csv')

CELL_WIDTH = 20
CELL_HEIGTH = 1

ARROWS = [
    260, 259, 261, 258
]

TABLE_COOR = (4, 1)

VIEW_SIZE = RangeAddress(Address('A1'), Address('A1'))
DEAFULT_NAME = 'spreadsheet.csv'
