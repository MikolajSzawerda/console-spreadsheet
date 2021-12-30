from src.Cells import Cell
from src.Addresses import Address, RangeAddress
from src.Errors import CellNotInSpreadsheetError


class Spreadsheet:
    def __init__(self, range: "RangeAddress" = None,
                 cells: "list[Cell]" = None,
                 command_cells=None,
                 localization=None):
        self._range = range
        self._cells = {}
        self.cells = cells

    @property
    def range(self) -> "RangeAddress":
        return self._range

    @property
    def cells(self) -> "dict[Address, Cell]":
        return self._cells

    @cells.setter
    def cells(self, val: "list[Cell]"):
        if val:
            val_dict = {x.address: x for x in val}
            self._cells = val_dict
        else:
            self._cells = {}

    def add_cells(self, cells: "list[Cell]"):
        if cells:
            val_dict = {x.address: x for x in cells}
            self._cells.update(val_dict)

    def remove_cells(self, addresses: "list[Address]"):
        try:
            for adr in addresses:
                self._cells.pop(adr)
        except KeyError:
            raise CellNotInSpreadsheetError(adr._address) from KeyError

    def cell(self, address: "Address"):
        return self.cells.get(address, Cell(address))

    def set_cell_val(self, address: "Address", val: "str"):
        if address not in self.cells.keys():
            self.add_cells([Cell(address, val)])
        else:
            self.cells[address].value = val

    def spreadsheet_view(self) -> "list[tuple[str, str]]":
        return [(str(x[0]), x[1].value) for x in self.cells.items()]
