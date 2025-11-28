from PySide6 import QtWidgets
from cell import Cell, CellTypes
from manifest import ManifestItem
from utils import get_sides

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
    
    def get_num_used_cells(self):
        used_count = 0
        grid = self.grid
        for row in grid:
            for item in row:
                used_count += int(item.get_type() == CellTypes.USED)
        
        return used_count

    # will check if layout is legal (no floating cells and must be symmetric)
    def valid_grid(self) -> bool:
        return self.is_symmetric() and self.is_physically_possible()

    # NAN layout must be mirror across port and starboard side
    def is_symmetric(self) -> bool:
        port_side, starboard_side = get_sides(self.get_grid())
        port_side_NANs = [] # FALSE not NAN, TRUE is NAN
        starboard_side_NANs = [] # FALSE not NAN, TRUE is NAN

        for row in port_side:
            row.reverse()
            for item in row:
                port_side_NANs.append(item.get_type() == CellTypes.NAN)

        for row in starboard_side:
            for item in row:
                starboard_side_NANs.append(item.get_type() == CellTypes.NAN)

        return port_side_NANs == starboard_side_NANs

    # no floating objects (USED ontop of UNUSED)
    def is_physically_possible(self) -> bool:
        row_count = self.get_row_count()
        col_count = self.get_col_count()
        grid = self.get_grid()

        for row in range(1,row_count):
            for col in range(col_count):
                if grid[row][col].get_type() == CellTypes.USED:
                    if grid[row-1][col].get_type() == CellTypes.UNUSED:
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