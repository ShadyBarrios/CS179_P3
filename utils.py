from PySide6 import QtWidgets
from manifest import ManifestItem
from enum import Enum
from cell import CellTypes
from pathlib import Path
    
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

def get_weight_list(grid:list[list[ManifestItem]]) -> list[int]:
    weights = []

    for row in grid:
        for item in row:
            if item.get_type() == CellTypes.USED:
                weights.append(item.get_weight())
    
    return weights

# criteria for false:
# 1) weight in list_one is not present in list_two (quantity matters)
# 2) after removing all weights in list_one from list_two, list_two is not empty
# def compare_weight_lists(list_one:list[int], list_two:list[int]) -> bool:
#     for weight in list_one:
#         if weight not in list_two:
#             return False
#         list_two.remove(weight)
    
#     return (len(list_two) == 0)