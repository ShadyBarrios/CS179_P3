import math

class Coordinate:
    def __init__(self, row:int, col:int):
        self.loc = (row, col)
    
    def get_row(self) -> int:
        return self.loc[0]

    def get_col(self) -> int:
        return self.loc[1]
    
    def __eq__(self, rhs):
        return (self.get_row() == rhs.get_row()) and (self.get_col() == rhs.get_col())