from manifest import ManifestItem
from enum import Enum
from action import ActionTypes
from cell import CellTypes

# used for manhattan dist calculation
class CraneMoves(Enum):
    MoveLeft = 1 # crane is to the right of the object (row doesn't matter)
    MoveRight = 2 # crane is to the left of the object (row doesn't matter)
    MoveDown = 3 # crane is above object
    MoveUp = 4 # crane has met a wall
    AtDest = 5 # crane is at dest
    MoveUpSameRow = 6 # crane is on the same row as object but met an obstacle (since our algo tracks what the crane can grab, it's actually a row above curr_row, so no need to count this move)

    def calculate_move(grid:list[list[ManifestItem]], curr_row:int, curr_col:int, target_row:int, target_col:int, actionType:ActionTypes):
        # print(f"{curr_row} {curr_col} | {target_row} {target_col}")
        if (((curr_row == target_row) ) and (curr_col == target_col)):
            return CraneMoves.AtDest
        
        if (curr_row > target_row) and (curr_col == target_col): # crane is above
            return CraneMoves.MoveDown
        
        if (curr_row == 8): # in park, but park is not destination
            return CraneMoves.MoveDown
        
        if (target_row == 8) and (curr_col == target_col): # crane is below park
            return CraneMoves.MoveUp
        
        if (curr_col < target_col): # crane is to left of item
            item_right = CellTypes.to_type(grid[curr_row][curr_col+1].get_title())
            if item_right != CellTypes.UNUSED:
                if curr_row == target_row and actionType == ActionTypes.ToItem:
                    return CraneMoves.MoveUpSameRow # shouldn't count this climb
                else:
                    return CraneMoves.MoveUp
            else:
                return CraneMoves.MoveRight # nothing in the way continue moving right
        
        if (curr_col > target_col): # crane is to right of item
            item_left = CellTypes.to_type(grid[curr_row][curr_col-1].get_title())
            if item_left != CellTypes.UNUSED:
                if curr_row == target_row and actionType == ActionTypes.ToItem:
                    return CraneMoves.MoveUpSameRow # shouldn't count this climb
                else:
                    return CraneMoves.MoveUp
            else:
                return CraneMoves.MoveLeft # nothing in the way continue moving left

    