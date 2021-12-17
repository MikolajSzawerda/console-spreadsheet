from src.Spreadsheets import Spreadsheet
from src.Cells import Cell
from src.Addresses import Address
from src.Errors import CellNotInSpreadsheetError
import pytest


def test_creating_spreadsheet():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1')),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4')),
        ])
    assert len(spr1.cells) == 4
    assert spr1.cells[Address('A3')].value == 3


def test_setting_cells_spreadsheet():
    spr1 = Spreadsheet()
    cells = [
        Cell(Address('A1')),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4')),
        ]
    spr1.cells = cells
    assert len(spr1.cells) == 4
    assert spr1.cells[Address('A3')].value == 3


def test_adding_cells():
    spr1 = Spreadsheet(cells=[Cell(Address('B1'), 3)])
    spr1.add_cells([
        Cell(Address('A1'), 2),
        Cell(Address('A2'), 'Hello world'),
        Cell(Address('A3'), 2),
    ])
    assert len(spr1.cells) == 4
    assert spr1.cells[Address('A2')].value == 'Hello world'


def test_removing_cells():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1')),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4')),
        ])
    spr1.remove_cells([Address('A4')])
    assert Cell(Address('A4')) not in spr1.cells.values()

    with pytest.raises(CellNotInSpreadsheetError):
        spr1.remove_cells([Address('A4')])


def test_setting_cell_val():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1')),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4')),
        ])
    spr1.set_cell_val(Address('A1'), 123)
    spr1.set_cell_val(Address('B2'), -12)
    assert spr1.cells[Address('A1')].value == 123
    assert spr1.cells[Address('B2')].value == -12


def test_spreadsheet_view():
    spr1 = Spreadsheet(cells=[
        Cell(Address('A1'), -2),
        Cell(Address('A2')),
        Cell(Address('A3'), 3),
        Cell(Address('A4'), 'hello world'),
        ])
    view = spr1.spreadsheet_view()
    test = [('A1', -2), ('A2', 0), ('A3', 3), ('A4', 'hello world')]
    assert view == test
