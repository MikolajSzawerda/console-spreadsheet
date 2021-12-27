from src.Cells import Cell
from src.Addresses import Address


def test_creating_cell():
    cell1 = Cell(Address('A1'))
    assert cell1.address == Address('A1')
    assert cell1.value == 0


def test_setting_cell_val():
    cell1 = Cell(Address('A1'), 2)
    cell1.value = 5
    assert cell1.value == 5

    cell1 = Cell(Address('A1'))
    cell1.value = -6
    assert cell1.value == -6

    cell1 = Cell(Address('A1'), 'excel')
    cell1.value = 'hello world'
    assert cell1.value == 'hello world'
