from solution import Solution
from node import Node
from queue import PriorityQueue
from state import State
from sys import maxsize as intmax # needed for bsf weight diff

def a_star_search(initial_state:State) -> Solution:
    frontier = PriorityQueue()

    first_run = True

    node_bsf:Node = None
    node_bsf_weight_diff:int = intmax # will be used to track

    # for fast lookup
    frontier_list = []
    explored = []

    start_state = initial_state.copy()
    start = Node(start_state.get_grid(), cost=0, heuristic=start_state.calculate_heuristic())

    frontier.put(start)
    frontier_list.append(start.get_state())

    while frontier:
        node:Node = frontier.get()
        print(f"Chose {node.get_action()} | {node.meets_criteria_b()}")
        node_weight_diff = node.get_weight_diff()
        
        if node.meets_criteria_b():
            return Solution(node)
        
        # since our heuristic is admissible and uses weight diff ((total weight * 10) - weight diff)
        #   if weight diff is increasing then that means that we have found a minimum
        if node_weight_diff > node_bsf_weight_diff:
            return Solution(node_bsf)

        # since time matters we only consider it bsf if its explicity <, not <=
        if node_weight_diff < node_bsf_weight_diff:
            node_bsf_weight_diff = node_weight_diff
            node_bsf = node

        frontier_list.remove(node.get_state())
        explored.append(node.get_state())

        # expand node and then add to frontier
        child:Node = None
        for child in sorted(node.generate_children()):
            child_state = child.get_state()

            # if first_run:
            #     print(f"{child.get_action()} | {child.get_total_cost()} | {child.get_heuristic()}")

            if child_state not in explored and child_state not in frontier_list:
                frontier.put(child)
                frontier_list.append(child.get_state())
        #         if first_run:
        #             print(f"ADDED: {child.get_action()} | {child.get_total_cost()} | {child.get_heuristic()}")
                    
        
        # first_run = False
        # break

    # if full frontier examined then that means last node is minimum
    return Solution(node_bsf)