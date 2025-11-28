from manifest import ManifestItem, ItemPosition
from cell import CellTypes
from utils import get_sides, get_weight_list, compare_weight_lists

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
    
    # in order for two grid to be "equal"
    # they must have the same quantity of each type of weight on the same or mirror each other
    #TODO: Need to fix, stacked weights is not the same as non-stacked weights
    # ex)
    # - 2 -         - - - 
    # - 1 -    !=   2 1 - because 1 can move on the right but not the left... compare columns?
    def __eq__(self, rhs):
        if not isinstance(rhs, State):
            return False
        
        this_grid = self.get_grid()
        rhs_grid = rhs.get_grid()

        this_port, this_starboard = get_sides(this_grid)
        rhs_port, rhs_starboard = get_sides(rhs_grid)

        this_port_weights = get_weight_list(this_port)
        rhs_port_weights = get_weight_list(rhs_port)

        if compare_weight_lists(this_port_weights, rhs_port_weights) == False:
            return False
        
        this_starboard_weights = get_weight_list(this_starboard)
        rhs_starboard_weights = get_weight_list(rhs_starboard)

        if compare_weight_lists(this_starboard_weights, rhs_starboard_weights) == False:
            return False

        # the grid can also be considered equal if they mirro each other
        mirrored_weights = compare_weight_lists(this_port_weights, rhs_starboard_weights)
        # split for readability (too long of a line)
        mirrored_weights = mirrored_weights and compare_weight_lists(this_starboard_weights, rhs_port_weights)

        return mirrored_weights
    
