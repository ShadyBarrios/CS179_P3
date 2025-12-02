from action import Action
from node import Node

class Solution:
    def __init__(self, goal_node:Node):
        self.goal_node = goal_node
        self.actions = self.get_actions()

    # returns actions in order
    def get_actions(self) -> list[Action]:
        actions = []
        current_node = self.goal_node

        while True:
            if current_node is None or current_node.get_action() is None:
                break
            actions.append(current_node.get_action())
            current_node = current_node.get_parent()

        actions.reverse()
        return actions
    
    # return nodes in reversed order
    def get_nodes(self) -> list[Node]:
        current_node = self.goal_node
        nodes = []
        while current_node is not None:
            nodes.append(current_node)
            current_node = current_node.parent
        nodes.reverse()
        return nodes
    
    def __str__(self) -> str:
        output = f"Num of moves: {self.num_actions()}:\n"
        for action in self.get_actions():
            output += f"{action}\n"
        
        return output
    
    def num_actions(self) -> int:
        return len(self.actions)
    