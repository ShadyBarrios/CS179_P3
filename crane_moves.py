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
        print(f"{curr_row} {curr_col} | {target_row} {target_col}")
        if (curr_row == target_row+1) and (curr_col == target_col):
            return CraneMoves.AtDest
        
        if (curr_row > target_row) and (curr_col == target_col): # crane is above
            return CraneMoves.MoveDown
        
        if (curr_row == 8): # in park, but park is not destination
            return CraneMoves.MoveDown
        
        if (target_row == 8) and (curr_col == target_col): # crane is below park
            return CraneMoves.MoveUp
        
        if (curr_row == target_row):
            if (curr_col == target_col - 1): # crane is directly to left of item
                return CraneMoves.MoveRight
            elif (curr_col == target_col + 1): # crane is directly to right of item
                return CraneMoves.MoveLeft
    
        # curr cannot be below target and in same column, so out of bounds is prevented
        
        item_left = CellTypes.to_type(grid[curr_row][curr_col-1].get_title())
        item_right = CellTypes.to_type(grid[curr_row][curr_col+1].get_title())
        
        if (curr_col < target_col): # crane is to left of item
            if item_right != CellTypes.UNUSED:
                return CraneMoves.MoveUp # wall in the way, climb up
            else:
                return CraneMoves.MoveRight # nothing in the way continue moving right
        
        if (curr_col > target_col): # crane is to right of item
            if item_left != CellTypes.UNUSED:
                return CraneMoves.MoveUp # wall in the way, climb up
            else:
                return CraneMoves.MoveLeft # nothing in the way continue moving left

    