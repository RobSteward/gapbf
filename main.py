from dfs import dfs
from PathHandler import ADBHandler
from PathHandler import DummyHandler
from config import graph, attempt_counter, path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes, attempt_delay

if __name__ == "__main__":
    path_counter = 0
    dfs(graph, DummyHandler(), path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print("\nReached end of paths to try. Exiting. See log.csv for results.")