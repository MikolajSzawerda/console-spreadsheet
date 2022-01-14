from src.Commands import CommandInterpreter
from src.Addresses import Address
from src.Cells import Cell
from src.Spreadsheets import Spreadsheet
import pytest


def test_getting_cell_value():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1'), 1),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4'), 4),
        Cell(Address('A6'), "Hello World"),
        ])
    inter = CommandInterpreter(spr1)
    assert inter.parse_command('A4') == 4
    assert inter.parse_command('A2') == 0
    assert inter.parse_command('A5') == 0
    assert inter.parse_command('A6') == "Hello World"


def test_setting_cell_text():
    spr1 = Spreadsheet()
    inter = CommandInterpreter(spr1)
    inter.parse_command('A1="3"')
    assert spr1.cell(Address('A1')).value == '"3"'
    inter.parse_command('A1="5"')
    assert spr1.cell(Address('A1')).value == '"5"'
    inter.parse_command('A1="very long uninteresting text"')
    assert spr1.cell(Address('A1')).value == '"very long uninteresting text"'


def test_setting_cell_number():
    spr1 = Spreadsheet()
    inter = CommandInterpreter(spr1)
    inter.parse_command('A1=3')
    assert spr1.cell(Address('A1')).value == 3
    inter.parse_command('A1=-5')
    assert spr1.cell(Address('A1')).value == -5
    inter.parse_command('A1=0')
    assert spr1.cell(Address('A1')).value == 0
    inter.parse_command('A1=1.25')
    assert spr1.cell(Address('A1')).value == pytest.approx(1.25)
    inter.parse_command('A1=-0.95')
    assert spr1.cell(Address('A1')).value == pytest.approx(-0.95)


def test_basic_numbers_operations():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A2'), 4),
        Cell(Address('A3'), -12),
        Cell(Address('B6'), 2),
        Cell(Address('C1'), 0),
        Cell(Address('D34'), '"Hello world"'),
        Cell(Address('D1'), 26),
    ])
    inter = CommandInterpreter(spr1)
    tests = [
        ('A1==5-2*(45-128)', 171),
        ('A1==2+5-6+8', 9),
        ('A1==2*7', 14),
        ('A1==10/5', 2),
        ('A1==10*3-10/3', pytest.approx(26.66666666)),
        ('A1==A2+A3-B6+2', -8),
        ('A1==A2-A3', 16),
        ('A1==A2', 4),
        ('A1==A2*A3-D1*C1 + A3', -60),
    ]
    for test in tests:
        inter.parse_command(test[0])
        assert spr1.cell(Address('A1')).value == test[1]


def test_commands_eval():
    spr1 = Spreadsheet(cells=[Cell(Address('B1'), -5)])
    inter = CommandInterpreter(spr1)
    inter.parse_command('A1==min(A1:B4)')
    assert spr1.cell(Address('A1')).value == -5


def test_commands_with_operations_eval():
    spr1 = Spreadsheet(cells=[
        Cell(Address('B1'), 5),
        Cell(Address('A1'), 4),
        Cell(Address('E1'), -4),
        Cell(Address('E2'), 6),
        ])
    inter = CommandInterpreter(spr1)
    inter.parse_command('D1==max(A1:B4)+2')
    assert spr1.cell(Address('D1')).value == 7
    inter.parse_command('D2==sum(A1:B4)-min(E1:E2)')
    assert spr1.cell(Address('D2')).value == 13
    inter.parse_command('D2==sum(A1:B1)*min(E1:E2)')
    assert spr1.cell(Address('D2')).value == -36


def test_commands_update():
    spr1 = Spreadsheet(cells=[
        Cell(Address('B1'), 5),
        Cell(Address('A1'), 4),
        Cell(Address('E1'), -4),
        Cell(Address('E2'), 6),
        ])
    inter = CommandInterpreter(spr1)
    inter.parse_command('D1==B1+A1')
    assert spr1.cell(Address('D1')).value == 9
    inter.parse_command('A1=5')
    assert spr1.cell(Address('D1')).value == 10
