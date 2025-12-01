from action import Action, ActionTypes, copy_grid
from manifest import ManifestItem, ItemPosition
from cell import CellTypes
from coordinate import Coordinate
from utils import get_sides, get_weight_list, compare_weight_lists, calculate_weight, compare_str_lists

class State:
    def __init__(self, grid: list[list[ManifestItem]], crane:Coordinate=Coordinate(9,1)):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
        self.crane = crane
    
    def __str__(self) -> str:
        output = ""
        grid = self.grid
        for row in grid:
            for item in row:
                output += str(item.get_weight()) + " "
            output += "\n"
        return output
    
    def copy(self):
        return State(copy_grid(self.grid))
    
    def copy_with_new_crane(self, crane:Coordinate):
        return State(copy_grid(self.grid), crane.copy())
    
    def get_crane(self) -> Coordinate:
        return self.crane
    
    def get_row_count(self) -> int:
        return self.row_count
    
    def get_col_count(self) -> int:
        return self.col_count
    
    def get_grid(self) -> list[list[ManifestItem]]:
        return self.grid
    
    def get_open_spots(self) -> list[ManifestItem]:
        return Action.get_open_spots(self.get_grid())
    
    def get_moveable_items(self) -> list[ManifestItem]:
        return Action.get_moveable_items(self.get_grid())

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
                if CellTypes.to_type(self.grid[row][col].get_title()) != CellTypes.UNUSED:
                    if CellTypes.to_type(self.grid[row-1][col].get_title()) == CellTypes.UNUSED:
                        return False

        return True

    # will check if layout is legal (no floating cells and must be symmetric)
    def valid_grid(self) -> bool:
        return self.is_symmetric() and self.is_physically_possible()
    
    # in order for two grid to be not "equal"
    # they cannot have the same moveable objects in addition to the same objects on the same sides
    # they can also mirror each other
    def __eq__(self, rhs):
        if not isinstance(rhs, State):
            return False
        
        this_grid = self.get_grid()
        rhs_grid = rhs.get_grid()

        this_port, this_starboard = get_sides(this_grid)
        rhs_port, rhs_starboard = get_sides(rhs_grid)

        same_weights = State.compare_weights(this_port, this_starboard, rhs_port, rhs_starboard)
        same_moveable_objects = State.compare_moveable_objects(this_port, this_starboard, rhs_port, rhs_starboard)
        
        same_crane_position = self.get_crane() == rhs.get_crane()

        return same_weights and same_moveable_objects and same_crane_position
    
    # compares to see that both grids have the same weights on the same sides (or mirrored)
    def compare_weights(lhs_port, lhs_starboard, rhs_port, rhs_starboard) -> bool:
        lhs_port_weights = get_weight_list(lhs_port)
        lhs_starboard_weights = get_weight_list(lhs_starboard)
        rhs_port_weights = get_weight_list(rhs_port)
        rhs_starboard_weights = get_weight_list(rhs_starboard)

        port = compare_weight_lists(lhs_port_weights, rhs_port_weights)
        starboard = compare_weight_lists(lhs_starboard_weights, rhs_starboard_weights)
        normal = port and starboard

        # the grid can also be considered equal if they mirror each other
        port_mirrored = compare_weight_lists(lhs_port_weights, rhs_starboard_weights)
        # split for readability (too long of a line)
        starboard_mirrored = compare_weight_lists(lhs_starboard_weights, rhs_port_weights)
        mirrored = port_mirrored and starboard_mirrored

        return normal or mirrored

    # compares to see that both grids have the same moveable objects on the same sides (or mirrored)
    def compare_moveable_objects(lhs_port, lhs_starboard, rhs_port, rhs_starboard) -> bool:
        lhs_port_moveable_objects = [item.get_title() for item in Action.get_moveable_items(lhs_port)]
        lhs_starboard_moveable_objects = [item.get_title() for item in Action.get_moveable_items(lhs_starboard)]
        rhs_port_moveable_objects = [item.get_title() for item in Action.get_moveable_items(rhs_port)]
        rhs_starboard_moveable_objects = [item.get_title() for item in Action.get_moveable_items(rhs_starboard)]

        port = compare_str_lists(lhs_port_moveable_objects, rhs_port_moveable_objects)
        starboard = compare_str_lists(lhs_starboard_moveable_objects, rhs_starboard_moveable_objects)
        normal = port and starboard

        port_mirrored = compare_str_lists(lhs_port_moveable_objects, rhs_starboard_moveable_objects)
        starboard_mirrored = compare_str_lists(lhs_starboard_moveable_objects, rhs_port_moveable_objects)
        mirrored = port_mirrored and starboard_mirrored

        return normal or mirrored
    
    # calculates all the possible operations from the current state, based on actionType
    def generate_actions(self, actionType:ActionTypes) -> list[Action]:
        actions = []

        match(actionType):
            case ActionTypes.FromPark:
                park = Coordinate(9,1)
                park_item = ManifestItem(park,0,"PARK")
                moveable_items = self.get_moveable_items()
                for target in moveable_items:
                    actions.append(Action(park_item, target))
            case ActionTypes.ToItem:
                crane_item = ManifestItem(self.crane, 0, "CRANE")
                moveable_items = self.get_moveable_items()
                for target in moveable_items:
                    if crane_item == target:
                        continue
                    actions.append(Action(crane_item, target))
            case ActionTypes.MoveItem:
                crane_item = ManifestItem(self.crane, 0, "CRANE")
                open_spots = self.get_open_spots()
                for target in open_spots:
                    if crane_item.directly_below(target):
                        continue
                    actions.append(Action(crane_item, target))
            case ActionTypes.ToPark:
                park = Coordinate(9,1)
                park_item = ManifestItem(park, 0, "PARK")
                crane_item = ManifestItem(self.crane, 0, "CRANE")
                actions.append(Action(crane_item, park_item))
        
        return actions

    # swaps coordinates of source and target, returns a new state
    def move(self, action:Action, actionType:ActionTypes):
        new_crane = action.target.get_coordinate().copy()
        return State(action.execute_move(self.get_grid(), actionType), new_crane)
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10), so expected is |Ph-Sh| > (Sum(Po, So) * 0.1) therefore |Ph - Sh| - (sum(Po, So) * 10) > 0
    # therefore, an admissible heurstic would be |Ph - Sh| - (sum(Po, So) * 10)
    # however, this could be negative (when goal met) and h(n) must be >= 0, so h(n) = max(0, |Ph - Sh| - (sum(Po, So) * 10))
    def calculate_heuristic(self) -> float:
        criteria_b_calc = self.criteria_b()
        return max(0, criteria_b_calc)
    
    def get_side_weights(self) -> tuple[int, int]:
        port_side, starboard_side = get_sides(self.get_grid())

        port_side_weight = calculate_weight(port_side)
        starboard_side_weight = calculate_weight(starboard_side)

        return port_side_weight, starboard_side_weight


    def criteria_b(self) -> float:
        port_side_weight, starboard_side_weight = self.get_side_weights()

        side_diff = abs(port_side_weight - starboard_side_weight)
        total_weight = port_side_weight + starboard_side_weight
        return side_diff - (total_weight * 0.1)
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10) therefore |Ph - Sh| - (sum(Po, So) * 10) < 0
    def meets_criteria_b(self) -> bool:
        criteria_b_calc = self.criteria_b()
        return (criteria_b_calc < 0)
