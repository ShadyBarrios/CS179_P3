from PySide6 import QtWidgets
from cell import Cell, CellTypes

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
                
    def update(self, new_grid:list[list]):
        row_count = len(new_grid)
        col_count = len(new_grid[0])

        if row_count != self.row_count:
            print("Row count given is not correct for grid init")
            exit()

        if col_count != self.col_count:
            print("Col count given is not correct for grid init")
            exit()
        
        for row in range(row_count):
            for col in range(col_count):
                if new_grid[row][col] == "NAN":
                    type = CellTypes.NAN
                    value = ''
                elif new_grid[row][col] == "UNUSED":
                    type = CellTypes.UNUSED
                    value = ''
                else:
                    type = CellTypes.USED
                    value = new_grid[row][col]

                self.grid[row_count][col_count].setType(type)
                self.grid[row_count][col_count].setValue(value)
                self.grid[row_count][col_count].updateText()