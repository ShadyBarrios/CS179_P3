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

    def __str__(self):
        display_row = self.loc[0] # "8 -" for display
        display_col = self.loc[1] # "12 -" for display
        return f"[{display_row:02d},{display_col:02d}]"
    
    def copy(self):
        return Coordinate(self.loc[0], self.loc[1])