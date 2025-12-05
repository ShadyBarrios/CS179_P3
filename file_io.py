import re
from manifest import ManifestItem
from coordinate import Coordinate
from error import ParseErrorTypes

# TODO: create parse result class
# TODO: hash strings so its easy to look up?
# TODO: create log stuff and file output


def parse_file(file_name) -> list[ManifestItem] | ParseErrorTypes:
    x_format = "0[1-8]"
    y_format = "0[1-9]|1[0-2]"
    weight_format = "[0-9]{5}"
    # written in regex
    # explanation of regex match criteria
    # one [ followed by 01 through 08 followed by , followed by 01 through 12 followed by one ]
    # followed by one , and one space
    # followed by one { followed by five 0 through 9 followed by one }, if UNUSED or NAN, must be 5 zeros
    # followed by one , and one space
    # followed by any number of characters that contain at least one lowercase/capital letter
    expected_format = "\[0[1-8],(0[1-9]|1[0-2])\],\s\{[0-9]{5}\},\s.*[a-zA-Z]+.*"

    if file_name[-4:] != ".txt":
        print("ERROR: File must be .txt type.")
        return ParseErrorTypes.IncorrectFileType

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

                proper_format = not(re.search(expected_format, line) is None)

                if proper_format:
                    sections = line.split(", ")
                    coordinate_str = sections[0]
                    weight_str = sections[1]
                    title_str = sections[2]

                    coordinate_str_parts = coordinate_str.split(",")
                    row_coordinate = int(re.findall(x_format, coordinate_str_parts[0])[0])
                    col_coordinate = int(re.findall(y_format, coordinate_str_parts[1])[0])

                    if col_coordinate != current_col:
                        return ParseErrorTypes.IncorrectFileFormatting
                    if row_coordinate != current_row:
                        return ParseErrorTypes.IncorrectFileFormatting

                    coordinate = Coordinate(row_coordinate, col_coordinate)

                    current_col += 1

                    if current_col == 13:
                        current_col = 1
                        current_row += 1

                    weight = int(re.findall(weight_format, weight_str)[0])

                    title = title_str.strip()
                    
                    items.append(ManifestItem(coordinate, weight, title))
                    item_count += 1
                else:
                    return ParseErrorTypes.IncorrectFileFormatting
                
            if item_count != 96:
                return ParseErrorTypes.IncorrectManifestLength
                
            return items
    except FileNotFoundError:
        print("ERROR: FILE NOT FOUND")
        return ParseErrorTypes.FileNotFound