from state import State
from manifest import ManifestItem
from solution import Solution
from node import Node
from queue import PriorityQueue

def a_star_search(initial_state: Node) -> Solution:
    frontier = PriorityQueue()

    # for fast lookup
    frontier_set = set()
    explored = set()

    start_state = initial_state.get_state()
    start = Node(start_state.get_grid(), cost=0, heuristic=start_state.calculate_heuristic())

    
