from cell import Cell, ParkCell
from manifest import ManifestItem
from state import State
from action import ActionTypes
from PySide6 import QtWidgets

class GridDisplay(State):
    def __init__(self, grid: list[list[ManifestItem]], parkLabel:QtWidgets.QLabel):
        super().__init__(grid, ActionTypes.FromPark)
        self.cell_grid: list[list[Cell]] = []
        self.parkCell = ParkCell(parkLabel)
        self.update()

    def update(self) -> None:
        self.cell_grid = []
        for row in self.grid:
            cell_row: list[Cell] = []
            for item in row:
                cell = Cell(item)
                style = cell.generate_style()
                cell.set_style(style)
                cell_row.append(cell)
            self.cell_grid.append(cell_row)
