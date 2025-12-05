from action import Action, ActionTypes
from cell import CellTypes
from coordinate import Coordinate
from manifest import ManifestItem

class State:
    def __init__(self, grid: list[list[ManifestItem]], crane: Coordinate=Coordinate(9,1)):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
        self.crane = crane
    
    def __str__(self) -> str:
        output = ""
        grid = self.grid
        for row in grid:
            for item in row:
                coordinate = f"{item.get_coordinate()}"
                weight = f"{item.get_weight():06d}"
                title = f"{item.get_title()}"
                output += coordinate + ", {" + weight + "}, " + title + "\n" 
        return output

    def _copy_grid(self) -> list[list[ManifestItem]]:
        grid_copy: list[list[ManifestItem]] = []
        for row in self.grid:
            copy_row: list[ManifestItem] = []
            for item in row:
                copy_row.append(item.copy())
            grid_copy.append(copy_row)
        return grid_copy

    def copy(self):
        grid_copy = self._copy_grid()
        crane_copy = self.crane.copy()
        return State(grid_copy, crane_copy)
    
    # def copy_with_new_crane(self, crane:Coordinate):
    #     return State(self._copy_grid(), crane.copy())
    
    def get_crane(self) -> Coordinate:
        return self.crane
    
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

    # Get list of all weights in grid
    def get_weight_list(self) -> list[int]:
        weights = []

        for row in range(self.row_count):
            for col in range(self.col_count):
                item = self.grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    weights.append(item.get_weight())

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
        crane_equality = self.__compare_cranes__(rhs)
        return column_equality and crane_equality
    
    def __hash__(self) -> int:
        port_weights, starboard_weights = self.get_side_weight_lists()

        # convert list[list[int]] to list[tuple[int]]
        port_weights_sorted = sorted([tuple(column) for column in port_weights])
        starboard_weights_sorted = sorted([tuple(column) for column in starboard_weights])

        # convert to tuple[tuple[int]]
        port_weights_final = tuple(port_weights_sorted)
        starboard_weights_final = tuple(starboard_weights_sorted)

        return hash((port_weights_final, starboard_weights_final, self.crane))

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
    
    def __compare_cranes__(self, rhs) -> bool:
        if not isinstance(rhs, State):
            return False
        return self.crane == rhs.get_crane()

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
                    if target.get_coordinate() == crane_item.get_coordinate():
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
    def move(self, action: Action, action_type: ActionTypes):
        new_grid = self._copy_grid()
        target_coordinate = action.target.get_coordinate().copy()
        
        match(action_type):
            case ActionTypes.FromPark:
                return State(new_grid, target_coordinate) 
            case ActionTypes.ToItem:
                return State(new_grid, target_coordinate)
            case ActionTypes.MoveItem:
                source_coordinate = action.source.get_coordinate().copy()


                source = new_grid[source_coordinate.get_row()-1][source_coordinate.get_col()-1].copy()
                source.set_coordinate(target_coordinate)

                # moves source object to target object
                new_grid[target_coordinate.get_row()-1][target_coordinate.get_col()-1] = source

                # update old source coordinate with empty object
                new_grid[source_coordinate.get_row()-1][source_coordinate.get_col()-1] = ManifestItem.empty_item(source_coordinate)
        
                return State(new_grid, target_coordinate)
            case ActionTypes.ToPark:
                return State(new_grid, target_coordinate)

    # criteria b: |Ph - Sh| < =(Sum(Po, So) * 0.10), so expected is |Ph-Sh| >= (Sum(Po, So) * 0.1) therefore |Ph - Sh| - (sum(Po, So) * 10) >= 0
    # therefore, an admissible heurstic would be |Ph - Sh| - (sum(Po, So) * 10)
    # however, this could be negative (when goal met) and h(n) must be >= 0, so h(n) = max(0, |Ph - Sh| - (sum(Po, So) * 10))
    # def calculate_heuristic(self) -> float:
    #     criteria_b_calc = self.criteria_b()
    #     return max(0, criteria_b_calc)

    def calculate_heuristic(self) -> int:
        result = 0
        port_side, starboard_side = self.get_sides()
        port_side_weight, starboard_side_weight = self.get_side_weights()
        total_weight = port_side_weight + starboard_side_weight

        balance_mass = total_weight//2

        side_containers = []
        if port_side_weight > starboard_side_weight:
            # Find all containers on a side
            deficit = balance_mass - starboard_side_weight
            for row in port_side:
                for item in row:
                    if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                        side_containers.append((item.get_col(), item.get_weight()))

            # Sort all containers on the side by weight in descending order
            side_containers.sort(key=lambda t: t[1], reverse=True)

            for column, weight in side_containers:
                # Find largest container(s) that are within criteria and accumulate their distance to centerline
                if weight <= deficit:
                    result += 7-column
                    break
            
        else:
            deficit = balance_mass - port_side_weight
            for row in starboard_side:
                for item in row:
                    if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                        side_containers.append((item.get_col(), item.get_weight()))
            
            # Sort all containers on the side by weight in descending order
            side_containers.sort(key=lambda t: t[1], reverse=True)
            
            for column, weight in side_containers:
                # Find largest container(s) that are within criteria and accumulate their distance to centerline
                if weight <= deficit:
                    result += column-6
                    break

        return result

    def calculate_criteria_a(self) -> int:
        # Ref: https://www.geeksforgeeks.org/dsa/partition-a-set-into-two-subsets-such-that-the-difference-of-subset-sums-is-minimum/
        weight_list = self.get_weight_list()
        total_weight = sum(weight_list)
        target_weight = total_weight // 2

        dp = [[False for _ in range(total_weight+1)] for _ in range(len(weight_list)+1)]

        dp[0][0] = True

        for i in range(1, len(weight_list)+1):
            for sum_value in range(total_weight+1):
                # skip
                dp[i][sum_value] = dp[i-1][sum_value]

                if sum_value >= weight_list[i-1]:
                    dp[i][sum_value] = dp[i][sum_value] or dp[i-1][sum_value - weight_list[i-1]]
        
        res = float('inf')

        for sum_val in range(target_weight+1):
            if dp[len(weight_list)][sum_val]:
                res = min(res, abs(total_weight - sum_val) - sum_val)
        
        return res

    def calculate_criteria_b(self) -> float:
        port_side_weight, starboard_side_weight = self.get_side_weights()

        side_diff = abs(port_side_weight - starboard_side_weight)
        total_weight = port_side_weight + starboard_side_weight
        return side_diff - (total_weight * 0.1)
    
    def meets_criteria_a(self) -> bool:
        port_weight, starboard_weight = self.get_side_weights()
        return abs(port_weight - starboard_weight) == self.calculate_criteria_a()

    # criteria b: |Ph - Sh| <= (Sum(Po, So) * 0.10) therefore |Ph - Sh| - (sum(Po, So) * 10) <= 0
    def meets_criteria_b(self) -> bool:
        return (self.calculate_criteria_b() < 0)

