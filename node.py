from manifest import ManifestItem
from action import Action
from state import State
from utils import get_sides, calculate_weight

class Node:
    def __init__(self, grid:list[list[ManifestItem]], cost:int=0, heuristic:float=0, action:Action=None, children=None, parent=None):
        self.state = State(grid)
        self.cost = cost # g(n)
        self.heuristic = heuristic # h(n)
        self.action = action
        self.children = children
        self.parent = parent

        self.row_count = 8
        self.col_count = 12
    
    def __lt__(self, rhs):
        if not(isinstance(rhs, Node)):
            print("ERROR: Improper compare in node __lt__")
            return False
        
        return self.get_total_cost() < rhs.get_total_cost()
    
    def get_weights(self) -> tuple[int, int]:
        return self.state.get_weights()

    # f(n) = g(n) + h(n)
    def get_total_cost(self) -> float:
        return self.get_cost() + self.get_heuristic()

    def get_cost(self) -> int:
        return self.cost

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

        for action in current_state.actions():
            new_state = current_state.move(action)
            heuristic = new_state.calculate_heuristic()
            node = Node(new_state.get_grid(), (self.cost + action.manhattan_dist()), heuristic, action, parent=self)
            children.append(node)
        return children
    
    def meets_criteria_b(self) -> bool:
        return self.get_state().meets_criteria_b()
    
    def get_weight_diff(self) -> int:
        port_side_weight, starboard_side_weight = self.get_state().get_side_weights()
        return abs(port_side_weight - starboard_side_weight)
    

    


        
            

