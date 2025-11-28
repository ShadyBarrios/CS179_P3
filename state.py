from manifest import ManifestItem, ItemPosition
from cell import CellTypes

class State:
    def __init__(self, grid:list[list[ManifestItem]]):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
    
    def get_row_count(self) -> int:
        return self.row_count
    
    def get_col_count(self) -> int:
        return self.col_count
    
    def get_grid(self) -> list[list[ManifestItem]]:
        return self.grid

    def get_weights(self) -> tuple[int, int]:
        port_weight = 0
        starboard_weight = 0

        for row in self.grid:
            for item in row:
                if CellTypes.to_type(item.get_title()) != CellTypes.USED:
                    continue
                if item.get_position() == ItemPosition.PORT:
                    port_weight += item.get_weight()
                else:
                    starboard_weight += item.get_weight()
    
        return (port_weight, starboard_weight)
    
    # hashes board for lookup
    def __hash__(self):
        return hash(self.grid)
    
    def __eq__(self, rhs):
        if not isinstance(rhs, State):
            return False
        
        this_grid = self.get_grid()
        rhs_grid = rhs.get_grid()

        row_count = self.get_row_count()
        col_count = self.get_col_count()

        for row in range(row_count):
            for col in range(col_count):
                if this_grid[row][col] != rhs_grid[row][col]:
                    return False
                
        return True
    
