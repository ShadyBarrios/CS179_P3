from solution import Solution
from node import Node
from queue import PriorityQueue
from state import State

class Search():
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.initial_node = Node(initial_state)

    def a_star_search(self):
        print("Starting search")
        frontier = PriorityQueue()

        # first_run = True

        node_bsf: Node = None
        node_bsf_weight_diff = float('inf') # will be used to track
        node_bsf_cost = float('inf')

        # for fast lookup
        explored = set()

        print(f"Chose {self.initial_node.get_action()} | {self.initial_node.action_type} | {self.initial_node.get_weight_diff()} | {self.initial_node.meets_criteria_b()} | {self.initial_node.get_total_cost()}")
        frontier.put(self.initial_node)
        explored.add(self.initial_node)

        if self.initial_node.meets_criteria_b():
            return Solution(None)

        while not frontier.empty():
            node: Node = frontier.get()
            
            print(f"Chose {node.get_action()} | {node.action_type} | {node.get_weight_diff()} | {node.get_total_cost()}")
            node_weight_diff = node.get_weight_diff()
            node_cost = node.get_cost()
            
            if node.meets_criteria_b():
                return Solution(node.to_park())
            
            # # # since our heuristic is admissible and uses weight diff ((total weight * 10) - weight diff)
            # # #   if weight diff is increasing then that means that we have found a minimum
            # if node_weight_diff > node_bsf_weight_diff:
            #     print("woof")
            #     return Solution(node_bsf.to_park())

            # since time matters we only consider it bsf if its explicity <, not <=
            if node_weight_diff < node_bsf_weight_diff or (node_weight_diff == node_bsf_weight_diff and node_cost < node_bsf_cost):
                node_bsf_weight_diff = node_weight_diff
                node_bsf_cost = node_cost
                node_bsf = node

            explored.add(node)

            # expand node and then add to frontier
            child: Node = None
            for child in node.generate_children():
                # if first_run:
                #     print(f"{child.get_action()} | {child.get_total_cost()} | {child.get_heuristic()}")
               
               if child not in explored:
                   frontier.put(child)

            #         if first_run:
            #             print(f"ADDED: {child.get_action()} | {child.get_total_cost()} | {child.get_heuristic()}")
                        
            
            # first_run = False
            # break

        # if full frontier examined then that means last node is minimum
        return Solution(node_bsf.to_park())
