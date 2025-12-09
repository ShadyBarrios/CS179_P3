from solution import Solution
from node import Node
from queue import PriorityQueue
from state import State

class Search():
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.initial_node = Node(initial_state)
        self.criteria_a = self.initial_node.calculate_criteria_a()

    def _goal_test(self, node: Node) -> bool:
        meets_criteria_a = (node.get_weight_diff() == self.criteria_a)
        meets_criteria_b = node.meets_criteria_b()
        return meets_criteria_a or meets_criteria_b

    def a_star_search(self):
        print("Starting search")
        frontier = PriorityQueue()
        explored = set()

        print(f"Chose {self.initial_node.get_action()} | {self.initial_node.action_type} | {self.initial_node.get_weight_diff()} | {self.initial_node.meets_criteria_b()} | {self.initial_node.get_total_cost()}")
        frontier.put(self.initial_node)
        explored.add(self.initial_node)

        if self._goal_test(self.initial_node):
            return Solution(self.initial_node)

        while not frontier.empty():
            node: Node = frontier.get()
            
            print(f"Chose {node.get_action()} | {node.action_type} | {node.get_weight_diff()} | {node.get_total_cost()} | {node.get_cost()} | {node.get_heuristic()}")
            
            if self._goal_test(node):
                return Solution(node.to_park())

            explored.add(node)

            # expand node and then add to frontier
            child: Node = None
            for child in node.generate_children():
               if child not in explored:
                   frontier.put(child)

        # Minimum is accounted for in '_goal_test()' check
        return Solution(None)
