from src.Commands import Task, CommandInterpreter
from src.Addresses import Address
from src.Cells import Cell
from src.Spreadsheets import Spreadsheet


def test_getting_cell_value():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1'), 1),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4'), 4),
        ])
    inter = CommandInterpreter(spr1)
    assert inter.parse_command('A4') == 4
    assert inter.parse_command('A2') == 0
    assert inter.parse_command('A5') == 0


def test_setting_cell_value():
    spr1 = Spreadsheet()
    inter = CommandInterpreter(spr1)
    inter.parse_command('A1=3')
    assert spr1.cell(Address('A1')).value == '3'
    inter.parse_command('A1=5')
    assert spr1.cell(Address('A1')).value == '5'
    inter.parse_command('A1=very long uninteresting text')
    assert spr1.cell(Address('A1')).value == 'very long uninteresting text'
