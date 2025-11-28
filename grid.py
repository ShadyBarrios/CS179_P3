from PySide6 import QtWidgets
from cell import Cell, CellTypes
from manifest import ManifestItem

class Grid:
    def __init__(self, grid:list[list[Cell]], row_count=8, col_count=12):
        self.row_count = len(grid)
        self.col_count = len(grid[0])

        if row_count != self.row_count:
            print("Row count given is not correct for grid init")
            exit()

        if col_count != self.col_count:
            print("Col count given is not correct for grid init")
            exit()

        self.grid = grid

    def get_row_count(self) -> int:
        return self.row_count

    def get_col_count(self) -> int:
        return self.col_count

    def get_grid(self) -> list[list[Cell]]:
        return self.grid

    # will check if layout is physically possible (no floating items)
    def valid_grid(self) -> bool:
        grid = self.get_grid()
        rows = self.get_row_count()
        cols = self.get_col_count()

        for row in range(1,rows):
            for col in range(cols):
                item = grid[row][col]
                if item.get_type() == CellTypes.USED:
                    item_below = grid[row-1][col]
                    if item_below.get_type() != CellTypes.USED:
                        return False
        
        return True
                
    def update(self, new_grid:list[ManifestItem]):
        row_count = self.get_row_count()
        col_count = self.get_col_count()
        
        for row in range(row_count):
            for col in range(col_count):
                item = new_grid[(row * col_count) + col]
                if item.get_title() == "NAN":
                    type = CellTypes.NAN
                    value = ''
                elif item.get_title() == "UNUSED":
                    type = CellTypes.UNUSED
                    value = ''
                else:
                    type = CellTypes.USED
                    value = new_grid[(row * col_count) + col]

                self.grid[row][col].set_type(type)
                self.grid[row][col].set_value(value)
                self.grid[row][col].set_item(item)
                self.grid[row][col].update_text()