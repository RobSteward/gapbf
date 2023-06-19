from dfs import dfs
from try_path import try_path
from config import graph, attempt_counter, path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes, attempt_delay

if __name__ == "__main__":
    path_counter = [0]
    print(f"Printing paths starting with {path_prefix} of min length {path_min_length} and max length {path_max_length} and ending with {path_suffix} excluding {excluded_nodes}. Delay between attempts is {attempt_delay} ms.")
    dfs(graph, path_counter[0], lambda path: try_path(path, attempt_counter), path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print("Total number of potential paths: ", path_counter[0])
    dfs(graph, path_counter[0], lambda path: try_path(path, attempt_counter), path_min_length, path_max_length, path_prefix, path_suffix, excluded_nodes)
    print("\nReached end of paths to try. Exiting. See log.csv for results.")