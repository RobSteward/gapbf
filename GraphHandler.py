from PathHandler import PathHandler

class GraphHandler:
    def __init__(self, graph, neighbors):
        self.graph = graph
        self.neighbors = neighbors


    # Depth-first search recursive traversal of the graph,
    # which calls path_handler function on each path.
    # You can also specify the prefix from which to start
    # and the maximum path length.
    def dfs(self, path_handler: PathHandler, path_min_len = 4, path_max_len = 25, path_prefix = [], path_suffix=[], excluded_nodes = []):
        visited = set(path_prefix)
        
        def dfs_helper(self, node, path):
            path = list(path)
            path.append(node)
            visited.add(node)
            if len(path) >= path_min_len: 
                if path[-1] in path_suffix or len(path_suffix) == 0:
                    path_handler.try_path(path)

            if len(path) < path_max_len:        
                for neighbor in self.graph[node]:
                    if neighbor not in excluded_nodes:
                        if neighbor not in visited:
                            dfs_helper(neighbor, path)
            
            path.pop()
            visited.remove(node)
        
        if not path_prefix:
            for node in self.graph:
                if node not in visited:
                    dfs_helper(self, node, path_prefix)
        else:
            dfs_helper(self, path_prefix[-1], path_prefix[:-1])