from action import Action
from manifest import ManifestItem, ItemPosition
from cell import CellTypes
from copy import copy
from utils import get_sides, get_weight_list, compare_weight_lists, calculate_weight

class State:
    def __init__(self, grid: list[list[ManifestItem]]):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
    
    def get_row_count(self) -> int:
        return self.row_count
    
    def get_col_count(self) -> int:
        return self.col_count
    
    def get_grid(self) -> list[list[ManifestItem]]:
        return self.grid

    def get_num_used_cells(self) -> int:
        used_count = 0
        for row in self.grid:
            for item in row:
                used_count += int(CellTypes.to_type(item.get_title()) == CellTypes.USED)
        
        return used_count

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
    
    def get_open_spots(self) -> list[ManifestItem]:
        open_items = []
        for row in range(self.row_count-1):
            for col in range(self.col_count):
                item = self.grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    item_above = self.grid[row+1][col]
                    if CellTypes.to_type(item_above.get_title()) == CellTypes.UNUSED:
                        open_items.append(item_above)
        return open_items

    def get_movable_items(self) -> list[ManifestItem]:
        movable_items = []
        for row in range(self.row_count-1):
            for col in range(self.col_count):
                item = self.grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    item_above = self.grid[row+1][col]
                    if CellTypes.to_type(item_above.get_title()) == CellTypes.UNUSED:
                        movable_items.append(item)
        return movable_items

    # NAN layout must be mirror across port and starboard side
    def is_symmetric(self) -> bool:
        port_side, starboard_side = get_sides(self.grid)
        port_side_NANs = [] # FALSE not NAN, TRUE is NAN
        starboard_side_NANs = [] # FALSE not NAN, TRUE is NAN

        for row in port_side:
            row.reverse()
            for item in row:
                port_side_NANs.append(CellTypes.to_type(item.get_title()) == CellTypes.NAN)

        for row in starboard_side:
            for item in row:
                starboard_side_NANs.append(CellTypes.to_type(item.get_title()) == CellTypes.NAN)

        return port_side_NANs == starboard_side_NANs

    # no floating objects (USED ontop of UNUSED)
    def is_physically_possible(self) -> bool:
        row_count = self.get_row_count()
        col_count = self.get_col_count()

        for row in range(1,row_count):
            for col in range(col_count):
                if CellTypes.to_type(self.grid[row][col].get_title()) == CellTypes.USED:
                    if CellTypes.to_type(self.grid[row-1][col].get_title()) == CellTypes.UNUSED:
                        return False

        return True

    # will check if layout is legal (no floating cells and must be symmetric)
    def valid_grid(self) -> bool:
        return self.is_symmetric() and self.is_physically_possible()
    
    # hashes board for lookup
    def __hash__(self) -> int:
        return hash(self.grid)
    
    # in order for two grid to be "equal"
    # they must have the same quantity of each type of weight on the similar columns or mirror each other
    def __eq__(self, rhs) -> bool:
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
    
    # calculates all the possible operations from the current state
    def generate_actions(self) -> list[Action]:
        moveable_items = self.get_movable_items()
        open_spots = self.get_open_spots()

        actions = []

        for source in moveable_items:
            for target in open_spots:
                actions.append(Action(source, target))
        
        return actions

    # swaps coordinates of source and target, returns a new state
    def move(self, action:Action):
        source = copy(action.source)
        source_coordinate = source.get_coordinate()

        target = copy(action.target)

        source.set_coordinate(target.get_coordinate())
        target.set_coordinate(source_coordinate)

        new_grid = copy(self.grid)
        new_grid[source.get_row()-1][source.get_col()-1] = source
        new_grid[target.get_row()-1][target.get_col()-1] = target

        return State(new_grid)
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10) -> 0 < (sum(Po, So) * 10) - |Ph - Sh|
    # therefore, an admissible heurstic would be (sum(Po, So) * 0.10) - |Ph - Sh|
    # however, this could be negative and h(n) must be >= 0, so h(n) = max(0, (sum(Po, So) * 0.10) - |Ph-Sh|)
    def calculate_heuristic(self) -> float:
        criteria_b_calc = self.criteria_b()
        return max(0, criteria_b_calc)

    def criteria_b(self) -> float:
        port_side, starboard_side = get_sides(self.get_grid())

        port_side_weight = calculate_weight(port_side)
        starboard_side_weight = calculate_weight(starboard_side)

        side_diff = abs(port_side_weight - starboard_side_weight)
        total_weight = port_side_weight + starboard_side_weight

        return (total_weight*.10) - side_diff
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10) -> 0 < (sum(Po, So) * 10) - |Ph - Sh|
    # therefore a pass is (sum(Po, So) * 10) - |Ph - Sh| <= 0
    def meets_criteria_b(self) -> bool:
        criteria_b_calc = self.criteria_b()
        return (criteria_b_calc <= 0)

