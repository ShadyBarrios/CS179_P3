from action import Action, ActionTypes
from manifest import ManifestItem
from state import State
from utils import manhattan_dist
from coordinate import Coordinate

class Node:
    def __init__(self, grid: list[list[ManifestItem]], cost: int=0, heuristic: float=0, action: Action=None, children=None, parent=None, crane=Coordinate(9,1), actionType = ActionTypes.FromPark):
        self.state = State(grid, crane)
        self.cost = cost # g(n)
        self.heuristic = heuristic # h(n)
        self.action = action
        self.children = children
        self.parent = parent
        self.actionType = actionType
        self.crane = crane
        self.row_count = 8
        self.col_count = 12

    def __eq__(self, rhs):
        if not(isinstance(rhs, Node)):
            return False

        comp_states = self.state == rhs.state
        comp_actions = self.actionType == rhs.actionType

        return (comp_states and comp_actions)
    
    def __lt__(self, rhs):
        if not(isinstance(rhs, Node)):
            print("ERROR: Improper compare in node __lt__")
            return False
        
        return self.get_total_cost() < rhs.get_total_cost()
    
    def to_park(self):
        current_state = self.get_state()
        action = current_state.generate_actions(ActionTypes.ToPark)[0] # returns 1
        new_state = current_state.move(action, ActionTypes.ToPark)
        crane = action.target.get_coordinate().copy()
        heuristic = new_state.calculate_heuristic()
        node = Node(new_state.get_grid(), self.cost, heuristic, action, children=None, parent=self, crane=crane, actionType=ActionTypes.ToPark)
        node.add_cost(node.manhattan_dist())
        return node  

    def next_action_type(self) -> ActionTypes:
        if self.meets_criteria_b():
            return ActionTypes.ToPark

        match(self.actionType):
            case ActionTypes.FromPark:
                return ActionTypes.ToItem
            case ActionTypes.ToItem:
                return ActionTypes.MoveItem
            case ActionTypes.MoveItem:
                return ActionTypes.ToItem
            
    
    def get_weights(self) -> tuple[int, int]:
        return self.state.get_weights()

    # f(n) = g(n) + h(n)
    def get_total_cost(self) -> float:
        return self.get_cost() + self.get_heuristic()

    def get_cost(self) -> int:
        return self.cost
    
    def add_cost(self, cost:int):
        self.cost += cost

    def get_heuristic(self) -> float:
        return self.heuristic

    def get_children(self):
        children:list[Node] = self.children
        return children

    def get_parent(self):
        parent:Node = self.parent
        return parent

    def get_state(self) -> State:
        return self.state
    
    def get_action(self) -> Action:
        return self.action
    
    def generate_children(self):
        children:list[Node] = []

        current_state = self.get_state()

        action:Action = None
        next_action_type = self.next_action_type()
        actions = current_state.generate_actions(next_action_type)
        for action in actions:
            new_state = current_state.move(action, next_action_type)
            crane = action.target.get_coordinate().copy()
            heuristic = new_state.calculate_heuristic()
            node = Node(new_state.get_grid(), self.cost, heuristic, action, children=None, parent=self, crane=crane, actionType=next_action_type)
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
        
        print("calc distance")
        dist = manhattan_dist(grid, curr_row, curr_col, target_row, target_col)
        return dist
    
    # def to_park(self):
    #     state = self.get_state()
    #     cost = manhattan_dist(state.get_grid())
    #     to_park = Node(state.get_grid(), )
    #     pass