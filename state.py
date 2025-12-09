from action import Action
from cell import CellTypes
from coordinate import Coordinate
from enums import ActionTypes, CellTypes
from manifest import ManifestItem

class State:
    def __init__(self, grid: list[list[ManifestItem]], crane: Coordinate=Coordinate(9,1)):
        self.row_count = 8
        self.col_count = 12
        self.grid = grid
        self.crane = crane
    
    def __str__(self) -> str:
        output = ""
        for row in self.grid:
            for item in row:
                output += str(item) + "\n"
        return output[:-1]
    
    # in order for two grid to be not "equal"
    # they cannot have the same moveable objects in addition to the same objects on the same sides
    # they can also mirror each other
    def __eq__(self, rhs):
        if not isinstance(rhs, State):
            return False
        column_equality = self.__compare_weight_columns__(rhs)
        # crane_equality = self.__compare_cranes__(rhs)
        # return column_equality and crane_equality
        return column_equality
    
    def __hash__(self) -> int:
        port_weights, starboard_weights = self.get_side_weight_lists()

        # convert list[list[int]] to list[tuple[int]]
        port_weights_sorted = sorted([tuple(column) for column in port_weights])
        starboard_weights_sorted = sorted([tuple(column) for column in starboard_weights])

        # convert to tuple[tuple[int]]
        port_weights_final = tuple(port_weights_sorted)
        starboard_weights_final = tuple(starboard_weights_sorted)

        return hash((port_weights_final, starboard_weights_final))

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
                if item.get_type() == CellTypes.USED:
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
                if item.get_type() == CellTypes.USED:
                    if col < 6:
                        port_col_weights.append(item.get_weight())
                    else:
                        starboard_col_weights.append(item.get_weight())
            if port_col_weights:
                port_weights.append(port_col_weights)
            if starboard_col_weights:
                starboard_weights.append(starboard_col_weights)

        return port_weights, starboard_weights
    
    def get_open_spots(self) -> list[ManifestItem]:
        open_spots: list[ManifestItem] = []

        for row in range(self.row_count):
            for col in range(self.col_count):
                item = self.grid[row][col]
                item_type = item.get_type()
                item_below_type = CellTypes.USED if row == 0 else self.grid[row-1][col].get_type()
                if item_type == CellTypes.UNUSED and item_below_type != CellTypes.UNUSED:
                    open_spots.append(item)
        # print([str(item.coordinate) for item in open_spots])
        return open_spots
    
    def get_moveable_items(self) -> list[ManifestItem]:
        moveable_items: list[ManifestItem] = []

        for row in range(self.row_count):
            for col in range(self.col_count):
                item = self.grid[row][col]
                item_type = item.get_type()
                item_above_type = CellTypes.UNUSED if row == 7 else self.grid[row+1][col].get_type()
                if item_type == CellTypes.USED and item_above_type == CellTypes.UNUSED:
                    moveable_items.append(item)
        return moveable_items

    def get_num_used_cells(self) -> int:
        used_count = 0
        for row in self.grid:
            for item in row:
                used_count += int(item.get_type() == CellTypes.USED)
        
        return used_count

    # NAN layout must be mirror across port and starboard side
    def is_symmetric(self) -> bool:
        port_side, starboard_side = self.get_sides()
        port_side_NANs = [] # FALSE not NAN, TRUE is NAN
        starboard_side_NANs = [] # FALSE not NAN, TRUE is NAN

        for row in port_side:
            row.reverse()
            for item in row:
                port_side_NANs.append(item.get_type() == CellTypes.NAN)

        for row in starboard_side:
            for item in row:
                starboard_side_NANs.append(item.get_type() == CellTypes.NAN)

        return port_side_NANs == starboard_side_NANs

    # no floating objects (USED ontop of UNUSED)
    def is_physically_possible(self) -> bool:
        row_count = self.get_row_count()
        col_count = self.get_col_count()

        for row in range(1,row_count):
            for col in range(col_count):
                if self.grid[row][col].get_type() != CellTypes.UNUSED:
                    if self.grid[row-1][col].get_type() == CellTypes.UNUSED:
                        return False

        return True

    # will check if layout is legal (no floating cells and must be symmetric)
    def valid_grid(self) -> bool:
        return self.is_symmetric() and self.is_physically_possible() and self.contains_no_ghost_weights()
    
    # any cells that are NAN or UNUSED yet have weights attached
    def contains_no_ghost_weights(self) -> bool:
        for row in self.grid:
            for item in row:
                if (item.get_title() == "UNUSED" or item.get_title() == "NAN") and item.get_weight() > 0:
                    return False
        return True

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
                new_grid[source_coordinate.get_row()-1][source_coordinate.get_col()-1] = ManifestItem(source_coordinate, 0, "UNUSED")
                
                return State(new_grid, target_coordinate)
            case ActionTypes.ToPark:
                return State(new_grid, target_coordinate)

    # criteria b: |Ph - Sh| <= (Sum(Po, So) * 0.10), so expected is |Ph-Sh| >= (Sum(Po, So) * 0.1) 
    # therefore |Ph - Sh| - (sum(Po, So) * 10) >= 0
    # 1. calculate the deficit between the target weight and the lighter side
    # - This is the amount of weight that should be moved
    # - The manhattan distance of the containers that need to be moved is a good analog for minutes
    # - Distance to the center is a good way to underestimate the manhattan distance for admissibility
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
                    if item.get_type() == CellTypes.USED:
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
                    if item.get_type() == CellTypes.USED:
                        side_containers.append((item.get_col(), item.get_weight()))
            
            # Sort all containers on the side by weight in descending order
            side_containers.sort(key=lambda t: t[1], reverse=True)
            
            for column, weight in side_containers:
                # Find largest container(s) that are within criteria and accumulate their distance to centerline
                if weight <= deficit:
                    result += column-6
                    break

        return result
