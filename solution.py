from action import Action
from node import Node

class Solution:
    def __init__(self, goal_node:Node):
        self.goal_node = goal_node

    def __str__(self) -> str:
        output = f"Num of moves: {len(self.get_actions())}:\n"
        for action in self.get_actions():
            output += f"{action}\n"
        
        return output

    # returns actions in order
    def get_actions(self) -> list[Action]:
        actions = []
        current_node = self.goal_node

        while True:
            if current_node is None or current_node.get_action() is None:
                break
            actions.append(current_node.get_action().copy())
            current_node = current_node.get_parent()

        actions.reverse()
        return actions
    
    # return states in reversed order
    def get_states(self) -> list[Node]:
        current_node = self.goal_node
        states = []
        while current_node is not None:
            states.append(current_node.state.copy())
            current_node = current_node.parent
        states.reverse()
        return states
    
    def get_nodes(self) -> list[Node]:
        current_node = self.goal_node
        nodes = []
        while current_node is not None:
            nodes.append(current_node)
            current_node = current_node.parent
        nodes.reverse()
        return nodes
    
    def get_time_to_execute(self) -> int:
        return self.goal_node.get_cost()
    