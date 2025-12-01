from manifest import ManifestItem
from enum import Enum
from cell import CellTypes

# used for manhattan dist calculation
class CraneMoves(Enum):
    MoveLeft = 1 # crane is to the right of the object (row doesn't matter)
    MoveRight = 2 # crane is to the left of the object (row doesn't matter)
    MoveDown = 3 # crane is above object
    MoveUp = 4 # crane has met a wall
    AtDest = 5 # crane is at dest

    def calculate_move(grid:list[list[ManifestItem]], curr_row:int, curr_col:int, target_row:int, target_col:int):
        if (curr_row == target_row) and (curr_col == target_col):
            return CraneMoves.AtDest
        
        if (curr_row > target_row) and (curr_col == target_col):
            return CraneMoves.MoveDown
        
        # curr cannot be below target and in same column, so out of bounds is prevented
        
        item_left = CellTypes.to_type(grid[curr_row][curr_col-1])
        item_right = CellTypes.to_type(grid[curr_row][curr_col-1])
        
        if (curr_row == target_row) and (curr_col < target_col) and item_right == CellTypes.UNUSED:
            return CraneMoves.MoveRight
        
        if (curr_row == target_row) and (curr_col > target_col) and item_left == CellTypes.UNUSED:
            return CraneMoves.MoveLeft
        
        if item_right != CellTypes.UNUSED or item_left != CellTypes.UNUSED:
            return CraneMoves.MoveUp
    
        if curr_col < target_col:
            return CraneMoves.MoveRight
        elif curr_col > target_col:
            return CraneMoves.MoveLeft
    