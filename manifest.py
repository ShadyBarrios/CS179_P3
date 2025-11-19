from coordinate import Coordinate

class ManifestItem:
    def __init__(self, coordinate:Coordinate, weight:int, title:str):
        self.coordinate = coordinate
        self.weight = weight
        self.title = title

    def __eq__(self, rhs):
        return self.coordinate == rhs.coordinate
    
    def get_col(self):
        return self.coordinate.get_col()

    def get_row(self):
        return self.coordinate.get_row()

    def get_row_for_display(self):
        return (8 - self.coordinate.get_row())
    
    def get_title(self):
        return self.title
    
    def get_title_for_display(self):
        if self.get_title() == "UNUSED" or self.get_title == "NAN":
            return "UNUSED" # same length as "unused"
        elif len(self.get_title()) > 6:
            return self.get_title()[:5] + "..."
        else:
            return self.get_title()
    
    def get_weight(self):
        return self.weight
    
