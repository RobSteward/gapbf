from PathHandler import PathHandler    
    
    # Depth-first search recursive traversal of the graph,
    #  # which calls path_handler function on each path.
    # You can also specify the prefix from which to start
    # and the maximum path length.
class PathFinder:
    def __init__(self, graph, neighbors):
        self.graph = graph
        self.neighbors = neighbors
        self.__handlers = []

    @property
    def handlers(self):
        return self.__handlers

    def add_handler(self, handler: PathHandler):
        assert isinstance(handler, PathHandler)
        self.__handlers.append(handler)

    def dfs(self, path_min_len=4, path_max_len=25, path_prefix=[], path_suffix=[], excluded_nodes=[]):
        visited = set(path_prefix)

        def dfs_helper(node, path):
            path = list(path)
            path.append(node)
            visited.add(node)

            if len(path) >= path_min_len:
                if path[-1] in list(map(int, path_suffix)) or not path_suffix:
                    for handler in self.handlers:
                        handler.try_path(path)

            if len(path) < path_max_len:
                for neighbor in self.neighbors[str(node)]:
                    if neighbor not in excluded_nodes and neighbor not in visited:
                        dfs_helper(neighbor, path)

            path.pop()
            visited.remove(node)

        if not path_prefix:
            for node in self.graph:
                if node not in visited:
                    dfs_helper(node, path_prefix)
        else:
            dfs_helper(path_prefix[-1], path_prefix[:-1])