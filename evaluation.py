import time
import utils

from search import Search
from state import State

def get_state(file_name) -> State:
    manifest_list = utils.parse_file(f'examples/{file_name}')
    grid = utils.create_grid_from_list(manifest_list)
    state = State(grid)
    return state

if __name__ == "__main__":

    TEST_FILE = "ShipCase5.txt"
    N = 50

    # Set up trials
    initial_state = get_state(TEST_FILE)
    search = Search(initial_state)
    times = []

    # Execute search for N trials
    print(f"Running {N} Trials")
    for i in range(N):
        print(f"======TRIAL {i+1}=======")
        start_time = time.time()
        solution = search.a_star_search()
        end_time = time.time()
        times.append(end_time-start_time)
        print(solution)

        
    # Calculate average time
    avg_duration = sum(times) / len(times)
    print(f"Average search duration for {TEST_FILE} over {N} trials: {avg_duration}")

