from coordinate import Coordinate
from enum import Enum

class ItemPosition(Enum):
    PORT = 1
    STARBOARD = 2

class ManifestItem:
    def __init__(self, coordinate:Coordinate, weight:int, title:str):
        self.coordinate = coordinate
        self.weight = weight
        self.title = title

        if coordinate.get_col() <= 6:
            self.position = ItemPosition.PORT
        else:
            self.position = ItemPosition.STARBOARD

    # only the coordinate and weight matter for matching, no difference in state if title is different
    def __eq__(self, rhs) -> int:
        if not isinstance(rhs, ManifestItem):
            return False
        return ((self.get_coordinate() == rhs.get_coordinate()) and (self.get_weight() == rhs.get_weight()))
    
    def get_coordinate(self) -> Coordinate:
        return self.coordinate
    
    def get_col(self) -> int:
        return self.coordinate.get_col()

    def get_row(self) -> int:
        return self.coordinate.get_row()

    def get_row_for_display(self) -> int:
        return (8 - self.coordinate.get_row())
    
    def get_title(self) -> str:
        return self.title
    
    def get_title_for_display(self) -> str:
        if self.get_title() == "UNUSED" or self.get_title == "NAN":
            return "UNUSED" # same length as "unused"
        elif len(self.get_title()) > 6:
            return self.get_title()[:5] + "..."
        else:
            return self.get_title()
    
    def get_weight(self) -> int:
        return self.weight

    def get_position(self) -> ItemPosition:
        return self.position
    
