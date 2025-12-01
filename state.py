import copy

from action import Action
from manifest import ManifestItem, ItemPosition
from cell import CellTypes

class State:
    def __init__(self, grid: list[list[ManifestItem]]):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
    
    def __str__(self) -> str:
        output = ""
        grid = self.grid
        for row in grid:
            for item in row:
                output += str(item.get_weight()) + " "
            output += "\n"
        return output

    def copy(self):
        grid_copy: list[list[ManifestItem]] = []
        for row in self.grid:
            copy_row: list[ManifestItem] = []
            for item in row:
                copy_row.append(item.copy())
            grid_copy.append(copy_row)

        return State(grid_copy)
    
    def get_row_count(self) -> int:
        return self.row_count
    
    def get_col_count(self) -> int:
        return self.col_count
    
    def get_grid(self) -> list[list[ManifestItem]]:
        return self.grid

    # Get the total weights on the port and starboard sides
    def get_side_weights(self) -> tuple[int, int]:
        port_weight = 0
        starboard_weight = 0

        for row in range(self.row_count):
            for col in range(self.col_count):
                item = self.grid[row][col]
                if col < 6:
                    port_weight += item.get_weight()
                else:
                    starboard_weight += item.get_weight()
    
        return port_weight, starboard_weight
    
    # split grid into two lists, port and starboard (port, starboard)
    def get_sides(self) -> tuple[list[list[ManifestItem]], list[list[ManifestItem]]]:
        port_side = []
        starboard_side = []

        for row in range(self.row_count):
            port_side_row = []
            starboard_side_row = []
            for col in range(self.col_count):
                item = self.grid[row][col]
                if col < 6:
                    port_side_row.append(item)
                else:
                    starboard_side_row.append(item)
            port_side.append(port_side_row)
            starboard_side.append(starboard_side_row)
        
        return port_side, starboard_side

    # Get columns of weights for a specific grid
    def _get_weight_list(grid: list[list[ManifestItem]]) -> list[list[int]]:
        weights = []
        row_count = len(grid)
        col_count = len(grid[0])

        for col in range(col_count):
            col_weights = []
            for row in range(row_count):
                item = grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    col_weights.append(item.get_weight())
            if len(col_weights) > 0:
                weights.append(col_weights)

        return weights
    
    def get_side_weight_lists(self) -> tuple[list[list[int]], list[list[int]]]:
        port_weights = []
        starboard_weights = []

        for col in range(self.col_count):
            port_col_weights = []
            starboard_col_weights = []
            for row in range(self.row_count):
                item = self.grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    if col < 6:
                        port_col_weights.append(item.get_weight())
                    else:
                        starboard_col_weights.append(item.get_weight())
            if port_col_weights:
                port_weights.append(port_col_weights)
            if starboard_col_weights:
                starboard_weights.append(starboard_col_weights)

        return port_weights, starboard_weights

    
    # Get movable items for a specific grid
    def _get_movable_items(grid: list[list[ManifestItem]]) -> list[ManifestItem]:
        moveable_items: list[ManifestItem] = []
        row_count = len(grid)
        col_count = len(grid[0])

        for row in range(row_count):
            for col in range(col_count):
                item = grid[row][col]
                item_type = CellTypes.to_type(item.get_title())
                item_above_type = CellTypes.UNUSED if row == 7 else CellTypes.to_type(grid[row+1][col].get_title())
                if item_type == CellTypes.USED and item_above_type == CellTypes.UNUSED:
                    moveable_items.append(item)
        return moveable_items
    
    def get_open_spots(self) -> list[ManifestItem]:
        open_spots: list[ManifestItem] = []

        for row in range(self.row_count):
            for col in range(self.col_count):
                item = self.grid[row][col]
                item_type = CellTypes.to_type(item.get_title())
                item_below_type = CellTypes.USED if row == 0 else CellTypes.to_type(self.grid[row-1][col].get_title())
                if item_type == CellTypes.UNUSED and item_below_type != CellTypes.UNUSED:
                    open_spots.append(item)

        return open_spots
    
    def get_moveable_items(self) -> list[ManifestItem]:
        return State._get_movable_items(self.grid)

    def get_num_used_cells(self) -> int:
        used_count = 0
        for row in self.grid:
            for item in row:
                used_count += int(CellTypes.to_type(item.get_title()) == CellTypes.USED)
        
        return used_count

    # NAN layout must be mirror across port and starboard side
    def is_symmetric(self) -> bool:
        port_side, starboard_side = self.get_sides()
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
        column_equality = self.__compare_weight_columns__(rhs)
        return column_equality
    
    # compares to see that both grids have the same weight columns on the same sides (or mirrored)
    def __compare_weight_columns__(self, rhs) -> bool:
        if not isinstance(rhs, State):
            return False

        lhs_port_weights, lhs_starboard_weights = self.get_side_weight_lists()
        rhs_port_weights, rhs_starboard_weights = rhs.get_side_weight_lists()

        lhs_port_weights_sorted, lhs_starboard_weights_sorted = sorted(lhs_port_weights), sorted(lhs_starboard_weights)
        rhs_port_weights_sorted, rhs_starboard_weights_sorted = sorted(rhs_port_weights), sorted(rhs_starboard_weights)
        
        port_equality = (lhs_port_weights_sorted == rhs_port_weights_sorted)
        starboard_equality = (lhs_starboard_weights_sorted == rhs_starboard_weights_sorted)
        port_equality_mirrored = (lhs_port_weights_sorted == rhs_starboard_weights_sorted)
        starboard_equality_mirrored = (lhs_starboard_weights_sorted == rhs_port_weights_sorted)

        equal_columns = port_equality and starboard_equality 
        equal_columns_mirrored = port_equality_mirrored and starboard_equality_mirrored


        return equal_columns or equal_columns_mirrored

    # # Compares if both grids have the same movable items
    # # Not needed?
    # def __compare_movable_items__(self, rhs) -> bool:
    #     if not isinstance(rhs, State):
    #         return False
        
    #     lhs_port, lhs_starboard = self.get_sides()
    #     rhs_port, rhs_starboard = rhs.get_sides()

    #     lhs_port_movable = {item for item in State._get_movable_items(lhs_port)}
    #     lhs_starboard_movable = {item for item in State._get_movable_items(lhs_starboard)}
    #     rhs_port_movable = {item for item in State._get_movable_items(rhs_port)}
    #     rhs_starboard_movable = {item for item in State._get_movable_items(rhs_starboard)}

    #     port_equality = (lhs_port_movable == rhs_port_movable)
    #     starboard_equality = (lhs_starboard_movable == rhs_starboard_movable)
    #     port_equality_mirrored = (lhs_port_movable == rhs_starboard_movable)
    #     starboard_equality_mirrored = (lhs_starboard_movable == rhs_port_movable)
        
    #     equal_movable = port_equality and starboard_equality
    #     equal_movable_mirrored = port_equality_mirrored and starboard_equality_mirrored

    #     return equal_movable or equal_movable_mirrored
    
    # calculates all the possible operations from the current state
    def generate_actions(self) -> list[Action]:
        moveable_items = self.get_moveable_items()
        open_spots = self.get_open_spots()

        actions = []

        for source in moveable_items:
            for target in open_spots:
                if source.directly_below(target): # cannot float
                    continue
                actions.append(Action(source, target))
        
        return actions

    # swaps coordinates of source and target, returns a new state
    def move(self, action: Action):
        source = action.source.copy()
        target = action.target.copy()

        source_coordinate = source.get_coordinate().copy()
        target_coordinate = target.get_coordinate().copy()

        updated_grid = copy.deepcopy(self.grid)

        # moves source object to target object
        updated_grid[target_coordinate.get_row()-1][target_coordinate.get_col()-1] = source
        # update new target object's coordinates
        updated_grid[target_coordinate.get_row()-1][target_coordinate.get_col()-1].set_coordinate(target_coordinate)
        # update old source coordinate with empty object
        updated_grid[source_coordinate.get_row()-1][source_coordinate.get_col()-1] = ManifestItem.empty_item(source_coordinate)
        
        return State(updated_grid)
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10), so expected is |Ph-Sh| > (Sum(Po, So) * 0.1) therefore |Ph - Sh| - (sum(Po, So) * 10) > 0
    # therefore, an admissible heurstic would be |Ph - Sh| - (sum(Po, So) * 10)
    # however, this could be negative (when goal met) and h(n) must be >= 0, so h(n) = max(0, |Ph - Sh| - (sum(Po, So) * 10))
    def calculate_heuristic(self) -> float:
        return max(0, self.calculate_criteria_b())

    def calculate_criteria_b(self) -> float:
        port_side_weight, starboard_side_weight = self.get_side_weights()

        side_diff = abs(port_side_weight - starboard_side_weight)
        total_weight = port_side_weight + starboard_side_weight
        return side_diff - (total_weight * 0.1)
    
    # criteria b: |Ph - Sh| < (Sum(Po, So) * 0.10) therefore |Ph - Sh| - (sum(Po, So) * 10) < 0
    def meets_criteria_b(self) -> bool:
        return (self.calculate_criteria_b() < 0)

