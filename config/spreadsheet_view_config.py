from src.Addresses import Address, RangeAddress
from src.Spreadsheets import Spreadsheet

adr1 = 'A1'
adr2 = 'AAAAAAAAAAAAAAAAAA1000000000000000000000'


SPREADSHEET = Spreadsheet(RangeAddress(Address(adr1), Address(adr2)),
                          localization='spreadsheet.csv')
CELL_WIDTH = 20
CELL_HEIGTH = 1
ARROWS = [260, 259, 261, 258]
TABLE_COOR = (5, 1)
VIEW_SIZE = RangeAddress(Address('A1'), Address('A1'))
DEAFULT_NAME = 'spreadsheet.csv'
