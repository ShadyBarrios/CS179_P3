from manifest import ManifestItem
from action import Action
from state import State

class Node:
    def __init__(self, grid:list[list[ManifestItem]], cost:int, heuristic:float, action:Action=None, children=None, parent=None):
        self.state = State(grid)
        self.cost = cost # g(n)
        self.heuristic = heuristic # h(n)
        self.action = action
        self.children = children
        self.parent = parent

        self.row_count = 8
        self.col_count = 12
    
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
    
    def generate_children(self):
        children:list[Node] = []
        return children
    

    


    


        
            

