from manifest import ManifestItem
from cell import CellTypes
from enum import Enum
from utils import copy_grid

class ActionTypes(Enum):
    FromPark = 1
    ToItem = 2
    MoveItem = 3
    ToPark = 4

class Action:
    def __init__(self, source: ManifestItem, target: ManifestItem):
        self.source = source
        self.target = target
    
    def __str__(self) -> str:
        return f"Move {self.source.get_coordinate()} to {self.target.get_coordinate()}"
    
    def get_open_spots(grid:list[list[ManifestItem]]):
        open_spots:list[ManifestItem] = []
        row_count = len(grid)
        col_count = len(grid[0])

        for row in range(row_count):
            for col in range(col_count):
                item = grid[row][col]
                item_type = CellTypes.to_type(item.get_title())
                item_below_type = CellTypes.USED if row == 0 else CellTypes.to_type(grid[row-1][col].get_title())
                if item_type == CellTypes.UNUSED and item_below_type != CellTypes.UNUSED:
                    open_spots.append(item)

        return open_spots

    def get_moveable_items(grid:list[list[ManifestItem]]):
        # moveable_items = Action.get(Wanted.MoveableItems, grid)
        moveable_items:list[ManifestItem] = []
        row_count = len(grid)
        col_count = len(grid[0])

        for row in range(row_count):
            for col in range(col_count):
                item = grid[row][col]
                item_type = CellTypes.to_type(item.get_title())
                item_above_type = CellTypes.UNUSED if row == 7 else CellTypes.to_type(grid[row+1][col].get_title())
                if item_type == CellTypes.USED and item_above_type == CellTypes.UNUSED:
                    moveable_items.append(item)
        return moveable_items
    
    # TODO: UPDATE with action type for from and to park
    # moves source to target, replaces source with empty item (UNUSED)
    def execute_move(self, grid:list[list[ManifestItem]], actionType:ActionTypes) -> list[list[ManifestItem]]:
        source_copy = self.source.copy()
        target_copy = self.target.copy()

        grid_copy = copy_grid(grid)

        source_coordinate = source_copy.get_coordinate().copy()
        target_coordinate = target_copy.get_coordinate().copy()

        # moves source object to target object
        grid_copy[target_coordinate.get_row()-1][target_coordinate.get_col()-1] = source_copy
        # update new target object's coordinates
        grid_copy[target_coordinate.get_row()-1][target_coordinate.get_col()-1].set_coordinate(target_coordinate)
        # update old source coordinate with empty object
        grid_copy[source_coordinate.get_row()-1][source_coordinate.get_col()-1] = ManifestItem.empty_item(source_coordinate)
        
        return grid_copy
     