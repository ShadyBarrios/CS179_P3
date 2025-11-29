from manifest import ManifestItem, ItemPosition
from cell import CellTypes
from utils import get_sides, get_weight_list, compare_weight_lists, calculate_weight
from action import Action

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
    # they must have the same quantity of each type of weight on the similar columns or mirror each other
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
    
    def actions(self) -> list[Action]:
        moveable_items = Action.get_moveable_items(self.grid)
        open_spots = Action.get_open_spots(self.grid)

        actions = []

        for source in moveable_items:
            for target in open_spots:
                actions.append(Action(source, target))
        
        return actions
    
    def move(self, action:Action):
        new_grid = action.execute_move(self.get_grid())

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

