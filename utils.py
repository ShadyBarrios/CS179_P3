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

def get_file_root_name(file_name: str) -> str:
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

# think of it as FSM where source moves to target
def manhattan_dist(grid: list[list[ManifestItem]], curr_row: int, curr_col: int, target_row: int, target_col: int):
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

    dist -= int(dist != 0) # crane hover, so if it moves to target, then just -1
    return dist
