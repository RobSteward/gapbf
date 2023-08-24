from PathFinder import PathFinder
from PathHandler import DummyHandler
from PathHandler import ADBHandler
from PathHandler import PathHandler
from ConfigHandler import ConfigHandler

# Load config file
config = ConfigHandler('config.yaml')

# Assigning variables
grid_size = config.get_value('grid_size')
path_min_length = config.get_value('path_min_length')
path_max_length = config.get_value('path_max_length')
path_prefix = config.get_value('path_prefix')
path_suffix = config.get_value('path_suffix')
excluded_nodes = config.get_value('excluded_nodes')
attempt_delay = config.get_value('attempt_delay')
test_path = config.get_value('test_path')
stdout_normal = config.get_value('outputstrings.stdout_normal')
stdout_success = config.get_value('outputstrings.stdout_success')
stdout_error = config.get_value('outputstrings.stdout_error')


# Load graph based on grid size
  # See https://twrp.me/faq/openrecoveryscript.html
  # print(f"Received path '{path}'")
  # Define a dictionary with the substitutions
def default():
    return PathFinder.graphs[3]["graph"], PathFinder.graphs[3]["neighbors"]

def case_4():
    return PathFinder.graphs[4]["graph"], PathFinder.graphs[4]["neighbors"]

def case_5():
    return PathFinder.graphs[5]["graph"], PathFinder.graphs[5]["neighbors"]

def case_6():
    return PathFinder.graphs[6]["graph"], PathFinder.graphs[6]["neighbors"]

switch = {
    3: default,
    4: case_4,
    5: case_5,
    6: case_6
}

# Select correct graph and neighbors and initialize handlers
graph, neighbors = switch.get(grid_size, default)()
dummy_handler = DummyHandler(test_path)
adb_handler = ADBHandler()

# Run DFS
if __name__ == "__main__":
    print(f"\nCalculating possible paths...")
    
    path_finder.add_handler(dummy_handler)
    path_finder.dfs(path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print(f"Completed.\nAttemptign brute force with {dummy_handler.counter} possible paths...")
    # graph_handler.dfs(adb_handler, path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print(f"Reached end of paths to try. Exiting. See log.csv for results.")