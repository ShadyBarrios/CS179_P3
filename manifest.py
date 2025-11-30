from coordinate import Coordinate
from enum import Enum

class ItemPosition(Enum):
    PORT = 1
    STARBOARD = 2

class ManifestItem:
    def __init__(self, coordinate: Coordinate, weight: int, title: str):
        self.coordinate = coordinate
        self.weight = weight
        self.title = title
        self.position = ItemPosition.PORT if coordinate.get_col() <= 6 else ItemPosition.STARBOARD

    def copy(self):
        return ManifestItem(self.coordinate.copy(), self.weight, self.title)
    
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
    
    def get_title(self) -> str:
        return self.title

    def get_weight(self) -> int:
        return self.weight

    def get_position(self) -> ItemPosition:
        return self.position

    def set_coordinate(self, coordinate: Coordinate):
        self.coordinate = coordinate

    def directly_below(self, rhs):
        if not(isinstance(rhs, ManifestItem)):
            print("ERROR: Improper compare in directly_below")
            return False
        
        same_col = self.get_coordinate().get_col() == rhs.get_coordinate().get_col()
        row_under = (self.get_coordinate().get_row() == (rhs.get_coordinate().get_row() - 1))
        return (same_col and row_under)
    
    def empty_item(coordinate:Coordinate):
        return ManifestItem(coordinate, 0, "UNUSED")
