from action import Action
from cell import CellTypes
from coordinate import Coordinate
from enums import ActionTypes, CellTypes, CraneMoves
from state import State

class Node:
    def __init__(self, state: State, cost: int=0, dist: int=0, action: Action=None, parent=None, action_type = ActionTypes.FromPark):
        self.state = state
        self.cost = cost # g(n)
        self.heuristic = state.calculate_heuristic() # h(n)
        self.action = action
        self.dist = dist
        self.parent = parent
        self.action_type = action_type
        self.row_count = 8
        self.col_count = 12

    def __eq__(self, rhs):
        if not(isinstance(rhs, Node)):
            return False
        
        comp_states = self.state == rhs.state
        comp_actions = self.action_type == rhs.action_type
        return comp_states and comp_actions
    
    def __hash__(self) -> int:
        actionType = ActionTypes.ToItem if (self.action_type == ActionTypes.FromPark or self.action_type == ActionTypes.ToPark) else self.action_type
        return hash((self.state, actionType))
    
    def __lt__(self, rhs):
        if not(isinstance(rhs, Node)):
            print("ERROR: Improper compare in node __lt__")
            return False
        
        return self.get_total_cost() < rhs.get_total_cost()

    def to_park(self):
        current_state = self.state

        if current_state.crane == Coordinate(9,1): # already at park
            return self
        
        action = current_state.generate_actions(ActionTypes.ToPark)[0] # returns 1
        dist = self.manhattan_dist(action, ActionTypes.ToPark)
        new_state = current_state.move(action, ActionTypes.ToPark)
        node = Node(new_state, self.cost + dist, dist, action, parent=self, action_type=ActionTypes.ToPark)
        return node

    def next_action_type(self) -> ActionTypes:
        if self.meets_criteria_b():
            return ActionTypes.ToPark

        match(self.action_type):
            case ActionTypes.FromPark:
                return ActionTypes.ToItem
            case ActionTypes.ToItem:
                return ActionTypes.MoveItem
            case ActionTypes.MoveItem:
                return ActionTypes.ToItem

    def get_weight_diff(self) -> int:
        port_side_weight, starboard_side_weight = self.state.get_side_weights()
        return abs(port_side_weight - starboard_side_weight)
    
    # f(n) = g(n) + h(n)
    def get_total_cost(self) -> float:
        return self.cost + self.heuristic

    def get_cost(self) -> int:
        return self.cost
    
    def get_heuristic(self) -> float:
        return self.heuristic

    def get_parent(self):
        parent: Node = self.parent
        return parent

    def get_state(self) -> State:
        return self.state
    
    def get_action(self) -> Action:
        return self.action
    
    def generate_children(self):
        children: list[Node] = []

        current_state = self.state

        action: Action = None
        next_action_type = self.next_action_type()
        actions = current_state.generate_actions(next_action_type)
        for action in actions:
            dist = self.manhattan_dist(action, next_action_type)
            new_state = current_state.move(action, next_action_type)
            node = Node(new_state, self.cost+dist, dist, action, parent=self, action_type=next_action_type)
            children.append(node)
        return children
    
    # criteria a: weight difference between sides is minimized
    def calculate_criteria_a(self) -> int:
        # Ref: https://www.geeksforgeeks.org/dsa/partition-a-set-into-two-subsets-such-that-the-difference-of-subset-sums-is-minimum/
        weight_list = self.state.get_weight_list()
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
    
    # criteria b: |Ph - Sh| <= (Sum(Po, So) * 0.10) therefore |Ph - Sh| - (sum(Po, So) * 10) <= 0
    def calculate_criteria_b(self) -> float:
        port_side_weight, starboard_side_weight = self.state.get_side_weights()

        side_diff = abs(port_side_weight - starboard_side_weight)
        total_weight = port_side_weight + starboard_side_weight
        return side_diff - (total_weight * 0.1)
    
    def meets_criteria_b(self) -> bool:
        return self.calculate_criteria_b() < 0

    def calculate_move(self, curr_row: int, curr_col: int, target_row: int, target_col: int, action_type: ActionTypes):
        if curr_row == 8:
            if curr_col < target_col:
                return CraneMoves.MoveRight
            elif curr_col > target_col:
                return CraneMoves.MoveLeft
            elif curr_row == target_row: # and curr_col == target_col
                return CraneMoves.AtDest
            else: # curr_col == target_col
                return CraneMoves.MoveDown

            
        grid = self.state.get_grid()
        # print(f"{curr_row} {curr_col} | {target_row} {target_col}")
        if (((curr_row == target_row) ) and (curr_col == target_col)):
            return CraneMoves.AtDest
        
        if (curr_row > target_row) and (curr_col == target_col): # crane is above
            return CraneMoves.MoveDown
        
        if (target_row == 8) and (curr_col == target_col): # crane is below park
            return CraneMoves.MoveUp
        
        if (curr_col < target_col): # crane is to left of item
            item_right = grid[curr_row][curr_col+1].get_type()
            if item_right != CellTypes.UNUSED:
                if curr_row == target_row and action_type == ActionTypes.ToItem:
                    return CraneMoves.MoveUpSameRow # shouldn't count this climb
                else:
                    return CraneMoves.MoveUp
            else:
                return CraneMoves.MoveRight # nothing in the way continue moving right
        
        if (curr_col > target_col): # crane is to right of item
            item_left = grid[curr_row][curr_col-1].get_type()
            if item_left != CellTypes.UNUSED:
                if curr_row == target_row and action_type == ActionTypes.ToItem:
                    return CraneMoves.MoveUpSameRow # shouldn't count this climb
                else:
                    return CraneMoves.MoveUp
            else:
                return CraneMoves.MoveLeft # nothing in the way continue moving left
        
    # think of it as FSM where source moves to target
    def manhattan_dist(self, action: Action, action_type: ActionTypes) -> int:
        grid = self.state.get_grid()

        # - 1 for idx
        curr_row = action.source.get_row() - 1
        curr_col = action.source.get_col() - 1
        target_row = action.target.get_row() - 1
        target_col = action.target.get_col() - 1

        dist = 0 
        crane_move = self.calculate_move(curr_row, curr_col, target_row, target_col, action_type)

        moveDown = False
        afterMoveItem = False
        moveUpSameRow = False
        if curr_row != 8:
            afterMoveItem = (grid[curr_row][curr_col].get_type() == CellTypes.USED) and (action_type == ActionTypes.ToItem)
        
        # print(f"{crane_move} for {curr_row},{curr_col} to {target_row},{target_col}")
        while True:
            match(crane_move):
                # move right
                case CraneMoves.MoveRight:
                    curr_col += 1
                case CraneMoves.MoveLeft:
                    curr_col -= 1
                case CraneMoves.MoveDown:
                    curr_row -= 1
                    moveDown = True
                case CraneMoves.MoveUp:
                    curr_row += 1
                case CraneMoves.MoveUpSameRow:
                    curr_row += 1
                    moveUpSameRow = True # will be nullified later, -1 to climb, -1 to go back down
                case CraneMoves.AtDest:
                    break
            dist += 1
            crane_move = self.calculate_move(curr_row, curr_col, target_row, target_col, action_type)

        if moveUpSameRow: # takes precedence
            dist -= 1
        elif moveDown and afterMoveItem:
            dist += 1

        dist -= int(dist > 0 and action_type != ActionTypes.MoveItem) # crane hover, so if it moves to target, then just -1 
        return dist
    