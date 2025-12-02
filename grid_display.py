from cell import Cell, ParkCell, CellTypes, TargetTypes
from manifest import ManifestItem
from state import State
from node import Node
from action import Action, ActionTypes
from PySide6 import QtWidgets

class GridDisplay(State):
    def __init__(self, grid: list[list[ManifestItem]], parkLabel:QtWidgets.QLabel):
        super().__init__(grid, ActionTypes.FromPark)
        self.cell_grid: list[list[Cell]] = []
        self.parkCell = ParkCell(parkLabel)
        self.refresh()

    def refresh(self) -> None:
        self.cell_grid = []
        for row in self.grid:
            cell_row: list[Cell] = []
            for item in row:
                cell = Cell(item)
                cell.update_style()
                cell_row.append(cell)
            self.cell_grid.append(cell_row)
        
    
    def update(self, state:State, action:Action):
        grid = state.get_grid()
        source = action.source
        target = action.target

        for row in range(8):
            for col in range(12):
                item = grid[row][col]
                cell = self.cell_grid[row][col]

                cell.set_item(item)
                cell._set_label_text()
                cell.set_type(CellTypes.to_type(item.get_title()))
                cell.set_targetType(None)
        
        if source.coordinate == self.parkCell.coordinate:
            self.parkCell.update_park(TargetTypes.SOURCE)
            targetCell = self.cell_grid[target.get_row()-1][target.get_col()-1]
            targetCell.set_targetType(TargetTypes.TARGET)
        elif target.coordinate == self.parkCell.coordinate:
            sourceCell = self.cell_grid[source.get_row()-1][source.get_col()-1]
            sourceCell.set_targetType(TargetTypes.SOURCE)
            self.parkCell.update_park(TargetTypes.TARGET)
        else:
            self.parkCell.update_park(None)
            sourceCell = self.cell_grid[source.get_row()-1][source.get_col()-1]
            targetCell = self.cell_grid[target.get_row()-1][target.get_col()-1]
            sourceCell.set_targetType(TargetTypes.SOURCE)
            targetCell.set_targetType(TargetTypes.TARGET)
        
        for row in self.cell_grid:
            for cell in row:
                cell.update_style()


