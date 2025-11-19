import re
import os
from PySide6 import QtWidgets
from enum import Enum
from manifest_item import ManifestItem
from coordinate import Coordinate

class ErrorTypes(Enum):
    FileNotFound = 1
    IncorrectFileType = 2
    IncorrectFileFormatting = 3
    IncorrectManifestLength = 4

def parse_file(file_name) -> list[ManifestItem] | ErrorTypes:
    x_format = "0[1-8]"
    y_format = "0[1-9]|1[0-2]"
    weight_format = "[0-9]{5}"
    # written in regex
    # explanation of regex match criteria
    # one [ followed by 01 through 08 followed by , followed by 01 through 12 followed by one ]
    # followed by one , and one space
    # followed by one { followed by five 0 through 9 followed by one }
    # followed by one , and one space
    # followed by any number of characters that contain at least one lowercase/capital letter
    expected_format = "\[0[1-8],(0[1-9]|1[0-2])\],\s\{[0-9]{5}\},\s.*[a-zA-Z]+.*"

    if file_name[-4:] != ".txt":
        print("ERROR: File must be .txt type.")
        return ErrorTypes.IncorrectFileType

    current_row = 1
    current_col = 1
    item_count = 0

    items = []
    try:
        with open(file_name, "r") as file:
            while True:
                line = file.readline()
            
                # EOF
                if line == "":
                    break

                proper_format:bool = not (re.search(expected_format, line) is None)

                if proper_format:
                    sections = line.split(", ")
                    coordinate_str = sections[0]
                    weight_str = sections[1]
                    title_str = sections[2]

                    coordinate_str_parts = coordinate_str.split(",")
                    x_coordinate = int(re.findall(x_format, coordinate_str_parts[0])[0])
                    y_coordinate = int(re.findall(y_format, coordinate_str_parts[1])[0])

                    if x_coordinate != current_col:
                        return ErrorTypes.IncorrectFileFormatting
                    if y_coordinate != current_row:
                        return ErrorTypes.IncorrectFileFormatting

                    coordinate = Coordinate(x_coordinate, y_coordinate)
                    current_row += 1
                    current_col += 1

                    weight = int(re.findall(weight_format, weight_str)[0])

                    items.append(ManifestItem(coordinate, weight, title_str))
                    item_count += 1
                else:
                    return ErrorTypes.IncorrectFileFormatting
                
            if item_count != 96:
                return ErrorTypes.IncorrectManifestLength
                
            return items
    except FileNotFoundError:
        print("ERROR: FILE NOT FOUND")
        return ErrorTypes.FileNotFound
    
def get_all_children_items(item) -> list[QtWidgets.QWidget]:
    children = []

    itemIsWidget = isinstance(item, QtWidgets.QWidgetItem)
    itemIsLayout = isinstance(item, QtWidgets.QLayoutItem)
    
    if itemIsWidget:
        item = item.widget()
        return [item]
    elif itemIsLayout and itemIsWidget:
        child_count = item.count()

        for child_idx in range(child_count):
            children.extend(get_all_children_items(item.itemAt(child_idx)))
        return children
    else:
        return []

    
