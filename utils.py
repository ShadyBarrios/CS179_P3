from PySide6 import QtWidgets
from manifest import ManifestItem
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
