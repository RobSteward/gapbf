from config import STDOUT_NORMAL, STDOUT_SUCCESS, STDOUT_ERROR

def path_counter():
    path_counter[0] += 1
# Credit to https://github.com/psarna
# Depth-first search recursive traversal of the graph,
# which calls path_handler function on each path.
# You can also specify the prefix from which to start
# and the maximum path length.
def dfs(graph, path_counter, path_handler, path_min_len = 4, path_max_len = 25, path_prefix = [], path_suffix=[], excluded_nodes = []):
    visited = set(path_prefix)
    
    def dfs_helper(node, path):
        path.append(node)
        visited.add(node)
        if len(path) >= path_min_len: 
            if path[-1] in path_suffix or len(path_suffix) == 0:
                path_handler(path)
                path_counter

        if len(path) < path_max_len:        
            for neighbor in graph[node]:
                if neighbor not in excluded_nodes:
                    if neighbor not in visited:
                        dfs_helper(neighbor, path)
        
        path.pop()
        visited.remove(node)
    
    if not path_prefix:
        for node in graph:
            if node not in visited:
                dfs_helper(node, path_prefix)
    else:
        dfs_helper(path_prefix[-1], path_prefix[:-1])