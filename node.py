from action import Action, ActionTypes
from state import State
from utils import manhattan_dist
from coordinate import Coordinate

class Node:
    def __init__(self, state: State, cost: int=0, action: Action=None, parent=None, action_type = ActionTypes.FromPark):
        self.state = state
        self.cost = cost # g(n)
        self.heuristic = state.calculate_heuristic() # h(n)
        self.action = action
        self.parent = parent
        self.action_type = action_type
        self.row_count = 8
        self.col_count = 12

    def __eq__(self, rhs):
        if not(isinstance(rhs, Node)):
            return False

        comp_states = self.state == rhs.state

        comp_actions_crane_matters = (self.action_type == ActionTypes.MoveItem) and (rhs.action_type == ActionTypes.MoveItem) # both got done moving items
        
        comp_actions_crane_doesnt_matter = (self.action_type != ActionTypes.MoveItem) and (rhs.action_type != ActionTypes.MoveItem)

        comp_actions = self.action_type == rhs.action_type

        # return (comp_states and (comp_actions_crane_doesnt_matter or (comp_actions_crane_matters and comp_crane)))
        return (comp_states and comp_actions)
    
    def __hash__(self) -> int:
        return hash((self.state, self.action_type))
    
    def __lt__(self, rhs):
        if not(isinstance(rhs, Node)):
            print("ERROR: Improper compare in node __lt__")
            return False
        
        return self.get_total_cost() < rhs.get_total_cost()
    
    def to_park(self):
        current_state = self.get_state()
        action = current_state.generate_actions(ActionTypes.ToPark)[0] # returns 1
        new_state = current_state.move(action, ActionTypes.ToPark)
        node = Node(new_state, self.cost, action, parent=self, action_type=ActionTypes.ToPark)
        node.add_cost(node.manhattan_dist())
        return node

    def next_action_type(self) -> ActionTypes:
        if self.meets_criteria_b():
            print(f"Met by {self.get_action()}")
            return ActionTypes.ToPark

        match(self.action_type):
            case ActionTypes.FromPark:
                return ActionTypes.ToItem
            case ActionTypes.ToItem:
                return ActionTypes.MoveItem
            case ActionTypes.MoveItem:
                return ActionTypes.ToItem
            
    
    def get_weights(self) -> tuple[int, int]:
        return self.state.get_side_weights()

    # f(n) = g(n) + h(n)
    def get_total_cost(self) -> float:
        return self.cost + self.heuristic

    def get_cost(self) -> int:
        return self.cost
    
    def add_cost(self, cost:int):
        self.cost += cost

    def get_heuristic(self) -> float:
        return self.heuristic

    def get_parent(self):
        parent:Node = self.parent
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
            new_state = current_state.move(action, next_action_type)
            node = Node(new_state, self.cost, action, parent=self, action_type=next_action_type)
            node.add_cost(node.manhattan_dist())
            children.append(node)
        return children
    
    def is_goal_state(self) -> bool:
        criteria_b = self.get_state().meets_criteria_b()
        crane_parked = self.get_state().get_crane() == Coordinate(9,1)

        return criteria_b and crane_parked
    
    def meets_criteria_b(self) -> bool:
        return self.get_state().meets_criteria_b()
    
    def get_weight_diff(self) -> int:
        port_side_weight, starboard_side_weight = self.get_state().get_side_weights()
        return abs(port_side_weight - starboard_side_weight)
    
    def manhattan_dist(self) -> int:
        action = self.get_action()
        state = self.get_state()
        grid = state.get_grid()

        # - 1 for idx
        curr_row = action.source.get_row() - 1
        curr_col = action.source.get_col() - 1
        target_row = action.target.get_row() - 1
        target_col = action.target.get_col() - 1
        
        dist = manhattan_dist(grid, curr_row, curr_col, target_row, target_col)
        return dist
    
    # def to_park(self):
    #     state = self.get_state()
    #     cost = manhattan_dist(state.get_grid())
    #     to_park = Node(state.get_grid(), )
    #     pass