import math

class Coordinate:
    def __init__(self, x:int, y:int):
        self.loc = (x, y)
    
    def get_x(self) -> int:
        return self.loc[0]

    def get_y(self) -> int:
        return self.loc[1]
    
    def __eq__(self, rhs):
        return (self.get_x() == rhs.get_x()) and (self.get_y() == rhs.get_y())