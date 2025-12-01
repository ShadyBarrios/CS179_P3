from PySide6 import QtWidgets
from manifest import ManifestItem
from crane_moves import CraneMoves
from cell import CellTypes
from pathlib import Path
from action import ActionTypes

def get_all_children_items(item) -> list[QtWidgets.QWidget]:
    children = []

    itemIsWidgetItem = isinstance(item, QtWidgets.QWidgetItem)
    itemIsLayoutItem = isinstance(item, QtWidgets.QLayoutItem)
    itemIsLayout = isinstance(item, QtWidgets.QLayout)
    
    if itemIsWidgetItem:
        item = item.widget()
        return [item]
    elif (itemIsLayoutItem and itemIsWidgetItem) or itemIsLayout:
        child_count = item.count()

        for child_idx in range(child_count):
            children.extend(get_all_children_items(item.itemAt(child_idx)))
        return children
    else:
        return []

def get_file_root_name(file_name:str) -> str:
    return Path(file_name).stem

def create_grid_from_list(item_list: list[ManifestItem], row_count: int = 8, col_count: int = 12) -> list[list[ManifestItem]]:
    grid: list[list[ManifestItem]] = []
    for row in range(row_count):
        state_row = []
        for col in range(col_count):
            item = item_list[(row*(col_count) + col)]
            state_row.append(item)
        grid.append(state_row)
    return grid

# split grid into two lists, port and starboard (port, starboard)
def get_sides(grid:list[list]) -> tuple[list[list],list[list]]:
    row_count = 8
    col_count = 12

    port_side = []
    starboard_side = []

    for row in range(row_count):
        port_side_row = []
        starboard_side_row = []
        for col in range(col_count):
            if col < 6:
                port_side_row.append(grid[row][col])
            else:
                starboard_side_row.append(grid[row][col])
        port_side.append(port_side_row)
        starboard_side.append(starboard_side_row)
    
    return port_side, starboard_side

# return columns of weights
def get_weight_list(grid:list[list[ManifestItem]]) -> list[list[int]]:
    weights = []
    row_count = len(grid)
    col_count = len(grid[0])

    for col in range(col_count):
        col_weights = []
        for row in range(row_count):
            item = grid[row][col]
            if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                col_weights.append(item.get_weight())
        if len(col_weights) > 0:
            weights.append(col_weights)

    return weights

# criteria for false:
# 1) weight column in list_one is not present in list_two (quantity matters)
# 2) after removing all weight columns in list_one from list_two, list_two is not empty
def compare_weight_lists(list_one:list[list[int]], list_two:list[list[int]]) -> bool:
    for column in list_one:
        if column not in list_two:
            return False
        list_two.remove(column)

    return (len(list_two) == 0)


def calculate_weight(grid:list[list[ManifestItem]]) -> int:
    weight = 0

    for row in grid:
        for item in row:
            weight += item.get_weight()
    
    return weight

def compare_str_lists(list_one:list[str], list_two:list[str]) -> bool:
    for string in list_one:
        if string not in list_two:
            return False
        list_two.remove(string)
    
    return len(list_two) == 0

# think of it as FSM where source moves to target
def manhattan_dist(grid:list[list[ManifestItem]], curr_row:int, curr_col:int, target_row:int, target_col:int, actionType:ActionTypes):
    dist = 0 
    crane_move = CraneMoves.calculate_move(grid, curr_row, curr_col, target_row, target_col)

    while True:
        match(crane_move):
            # move right
            case CraneMoves.MoveRight:
                curr_col += 1
            case CraneMoves.MoveLeft:
                curr_col -= 1
            case CraneMoves.MoveDown:
                curr_row -= 1
            case CraneMoves.MoveUp:
                curr_row += 1
            case CraneMoves.AtDest:
                break
        dist += 1
        crane_move = CraneMoves.calculate_move(grid, curr_row, curr_col, target_row, target_col)
    
    return dist
