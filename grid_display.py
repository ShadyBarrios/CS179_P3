from cell import Cell
from manifest import ManifestItem
from state import State

class GridDisplay(State):
    def __init__(self, grid: list[list[ManifestItem]]):
        super().__init__(grid)
        self.cell_grid: list[list[Cell]] = []
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
