from coordinate import Coordinate

class ManifestItem:
    def __init__(self, coordinate:Coordinate, weight:int, title:str):
        self.coordinate = coordinate
        self.weight = weight
        self.title = title

    def __eq__(self, rhs):
        return self.coordinate == rhs.coordinate
    
