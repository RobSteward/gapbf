from PathFinder import PathFinder
from PathHandler import DummyHandler
from PathHandler import ADBHandler
from ConfigHandler import ConfigHandler

# Load config file
config = ConfigHandler('config.yaml')
#print("Grid size:", config.grid_size)
path_finder = PathFinder(config.grid_size)
#print("Graphs:", path_finder.graphs)
# Load graph based on grid size

def default():
    if 3 in path_finder.graphs:
        return path_finder.graphs[0][3]["graph"], path_finder.graphs[0][3]["neighbors"]
    else:
        raise ValueError("Unexpected grid size")

def case_4():
    return path_finder.graphs[0][4]["graph"], path_finder.graphs[0][4]["neighbors"]

def case_5():
    return path_finder.graphs[0][5]["graph"], path_finder.graphs[0][5]["neighbors"]

def case_6():
    return path_finder.graphs[0][6]["graph"], path_finder.graphs[0][6]["neighbors"]

switch = {
    3: default,
    4: case_4,
    5: case_5,
    6: case_6
}

# Select correct graph and neighbors and initialize handlers
graph, neighbors = switch.get(config.grid_size, default)()
dummy_handler = DummyHandler(config)
adb_handler = ADBHandler(config)

# Run main program
if __name__ == "__main__":
    print(f"\nCalculating possible paths...")
    path_finder.add_handler(dummy_handler)
    path_finder.add_handler(adb_handler)
    #path_finder.dfs(graph, neighbors, config.path_min_length, config.path_max_length, config.path_prefix, config.path_suffix, config.excluded_nodes)
    print(f"Completed. Attemptign brute force with {dummy_handler.counter} total possible paths...")
    path_finder.dfs(adb_handler, config.path_min_length, config.path_max_length, config.path_prefix, config.path_suffix, config.excluded_nodes)
    print(f"Reached end of paths to try. Exiting. See log.csv for results.")