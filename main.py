import json
from GraphHandler import GraphHandler
from PathHandler import DummyHandler
from PathHandler import ADBHandler
from PathHandler import PathHandler


# Load config file
with open('config.json') as config_file:
    data = json.load(config_file)

# Assigning variables
grid_size = data["config"]["grid_size"]
path_min_length = data["config"]["path_min_length"]
path_max_length = data["config"]["path_max_length"]
path_prefix = data["config"]["path_prefix"]
path_suffix = data["config"]["path_suffix"]
excluded_nodes = data["config"]["excluded_nodes"]
attempt_delay = data["config"]["attempt_delay"]
test_path = data["config"]["test_path"]
stdout_normal = data["config"]["outputstrings"]["stdout_normal"]
stdout_success = data["config"]["outputstrings"]["stdout_success"]
stdout_error = data["config"]["outputstrings"]["stdout_error"]


# Load graph based on grid size
  # See https://twrp.me/faq/openrecoveryscript.html
  # print(f"Received path '{path}'")
  # Define a dictionary with the substitutions
def default():
    return data["grids"]["3x3"]["graph"], data["grids"]["3x3"]["neighbors"]

def case_4x4():
    return data["grids"]["4x4"]["graph"], data["grids"]["4x4"]["neighbors"]

def case_5x5():
    return data["grids"]["5x5"]["graph"], data["grids"]["5x5"]["neighbors"]

def case_6x6():
    return data["grids"]["6x6"]["graph"], data["grids"]["6x6"]["neighbors"]

switch = {
    3: default,
    4: case_4x4,
    5: case_5x5,
    6: case_6x6
}

# Select correct graph and neighbors and initialize handlers
graph, neighbors = switch.get(grid_size, default)()
dummy_handler = DummyHandler(test_path)
adb_handler = ADBHandler()

# Run DFS
if __name__ == "__main__":
    print(f"\nCalculating possible paths...")
    graph_handler = GraphHandler(graph, neighbors)
    graph_handler.dfs(dummy_handler, path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print(f"Completed.\nAttemptign brute force with {dummy_handler.counter} possible paths...")
    # graph_handler.dfs(adb_handler, path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print(f"Reached end of paths to try. Exiting. See log.csv for results.")