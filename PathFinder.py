from typing import List, Union, Set, Tuple
from PathHandler import PathHandler   

    # See https://twrp.me/faq/openrecoveryscript.html
    # Define a dictionary with the substitutions
    # Sets configuration values with which to initiate PathFinder (graph and neighbors based on grid size)
    # Should have 1 property, 1 method to handle_path and 1 method to register handlers
class PathFinder:
    _graphs: dict = {
            3: {
                "graph": [1,2,3,4,5,6,7,8,9], 
                "neighbors": {
                "1": [2, 4, 5],
                "2": [1, 3, 4, 5, 6], 
                "3": [2, 5, 6],
                "4": [1, 2, 5, 7, 8],
                "5": [1, 2, 3, 4, 6, 7, 8, 9],
                "6": [2, 3, 5, 8, 9],
                "7": [4, 5, 8],
                "8": [4, 5, 6, 7, 9],
                "9": [5, 6, 8]
                }
            },
            4: {
                "graph": [1,2,3,4,5,6,7,8,9,":",";","<","=",">","?","@"],
                "neighbors": {
                "1": [2, 5, 6], 
                "2": [1, 3, 5, 6, 7],
                "3": [2, 4, 6, 7, 8],
                "4": [3, 7, 8],
                "5": [1, 2, 6, 9, ":"],
                "6": [1, 2, 3, 5, 7, 9, ":", ";"],
                "7": [2, 3, 4, 6, 8, ":", ";", "<"],
                "8": [3, 4, 7, ";", "<"],
                "9": [5, 6, ":", "=", ">"],
                ":": [5, 6, 7, 9, ";", "=", ">", "?"],
                ";": [6, 7, 8, ":", "<", ">", "?", "@"],
                "<": [7, 8, ";", "?", "@"],
                "=": [9, ":", ">"],
                ">": [9, ":", ";", "=", "?"],
                "?": [":", ";", "<", ">", "@"],
                "@": [";", "<", "?"]
                }
            },
            5: {
                "graph": [1,2,3,4,5,6,7,8,9,":",";","<","=",">","?","@","A","B","C","D","E","F","G","H","I"],
                "neighbors": {
                    "1": [2, 6, 7], 
                    "2": [1, 3, 6, 7, 8],
                    "3": [2, 4, 7, 8, 9],
                    "4": [3, 5, 8, 9, ":"],
                    "5": [4, 9, ":"],
                    "6": [1, 2, 7, ";", "<"],
                    "7": [1, 2, 3, 6, 8, ";", "<", "="],
                    "8": [2, 3, 4, 7, 9, "<", "=", ">"],
                    "9": [3, 4, 5, 8, ":", "=", ">", "?"],
                    ":": [4, 5, 9, ">", "?"],
                    ";": [6, 7, "<", "@", "A"],
                    "<": [6, 7, 8, ";", "=", "@", "A", "B"],
                    "=": [7, 8, 9, "<", ">", "A", "B", "C"],
                    ">": [8, 9, ":", "=", "?", "B", "C", "D"],
                    "?": [9, ":", ">", "C", "D"],
                    "@": [";", "<", "A", "E", "F"],
                    "A": [";", "<", "=", "@", "B", "E", "F", "G"],
                    "B": ["<", "=", ">", "A", "C", "F", "G", "H"],
                    "C": ["=", ">", "?", "B", "D", "G", "H", "I"],
                    "D": [">", "?", "C", "H", "I"],
                    "E": ["@", "A", "F"],
                    "F": ["@", "A", "B", "E", "G"],
                    "G": ["A", "B", "C", "F", "H"],
                    "H": ["B", "C", "D", "G", "I"],
                    "I": ["C", "D", "H"]
                }
            },
            6: {
                "graph": [1, 2, 3, 4, 5, 6, 7, 8, 9, ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                "neighbors": {
                    "1": [2, 7, 8],
                    "2": [1, 3, 7, 8, 9],
                    "3": [2, 4, 8, 9, ":"],
                    "4": [3, 5, 9, ":", ";"],
                    "5": [4, 6, ":", ";", "<"],
                    "6": [5, ";", "<"],
                    "7": [1, 2, 8, "=", ">"],
                    "8": [1, 2, 3, 7, 9, "=", ">", "?"],
                    "9": [2, 3, 4, 8, ":", ">", "?", "@"],
                    ":": [3, 4, 5, 9, ";", "?", "@", "A"],
                    ";": [4, 5, 6, ":", "<", "@", "A", "B"],
                    "<": [5, 6, ";", "A", "B"],
                    "=": [7, 8, ">", "C", "D"],
                    ">": [7, 8, 9, "=", "?", "C", "D", "E"],
                    "?": [8, 9, ":", ">", "@", "D", "E", "F"],
                    "@": [9, ":", ";", "?", "A", "E", "F", "G"],
                    "A": [":", ";", "<", "@", "B", "F", "G", "H"],
                    "B": [";", "<", "A", "G", "H"],
                    "C": ["=", ">", "D", "I", "J"],
                    "D": ["=", ">", "?", "C", "E", "I", "J", "K"],
                    "E": [">", "?", "@", "D", "F", "J", "K", "L"],
                    "F": ["?", "@", "A", "E", "G", "K", "L", "M"],
                    "G": ["@", "A", "B", "F", "H", "L", "M", "N"],
                    "H": ["A", "B", "G", "M", "N"],
                    "I": ["C", "D", "J", "O", "P"],
                    "J": ["C", "D", "E", "I", "K", "O", "P", "Q"],
                    "K": ["D", "E", "F", "J", "L", "P", "Q", "R"],
                    "L": ["E", "F", "G", "K", "M", "Q", "R", "S"],
                    "M": ["F", "G", "H", "L", "N", "R", "S", "T"],
                    "N": ["G", "H", "M", "S", "T"],
                    "O": ["I", "J", "P"],
                    "P": ["I", "J", "K", "O", "Q"],
                    "Q": ["J", "K", "L", "P", "R"],
                    "R": ["K", "L", "M", "Q", "S"],
                    "S": ["L", "M", "N", "R", "T"],
                    "T": ["M", "N", "S"]
                }
            },
        }

    def __init__(self, grid_size: int, path_min_len: int = 4, path_max_len: int = 36, path_max_node_distance: int = 1, path_prefix: Tuple[Union[int, str]] = [], path_suffix: Tuple[Union[int, str]] = [], excluded_nodes: Set[Union[int, str]] = []):
        if grid_size not in self._graphs:
            raise ValueError(
                f'Invalid grid_size: {grid_size}. Available sizes are: {list(self._graphs.keys())}')
        self._grid_size = grid_size
        graph_data = self._graphs.get(self._grid_size, {})
        self._graph = graph_data.get("graph", [])
        self._neighbors = graph_data.get("neighbors", {})
        self.__handlers = []  # TODO: Should this be double underscore?
        self._total_paths = None
        self._path_min_len = path_min_len
        self._path_max_len = path_max_len
        self._path_max_node_distance = path_max_node_distance
        self._path_prefix = tuple(path_prefix)
        self._path_suffix = tuple(path_suffix)
        self._excluded_nodes = set(excluded_nodes)

    @property
    def handlers(self):
        return self.__handlers
    
    @property
    def total_paths(self):
        if self._total_paths is None:
            self._total_paths = self._calculate_total_paths()
        return self._total_paths
    
    def add_handler(self, handler: PathHandler) -> bool:
        if not isinstance(handler, PathHandler):
            raise TypeError("Expected a PathHandler instance.")
        self.__handlers.append(handler)
        
    def process_path(self, path):
        for handler in self.handlers:
            success, _path = handler.handle_path(path)
            if not success:
                return False, None
            return True, _path
    
    def _calculate_total_paths(self) -> int:
        visited = set(self._path_prefix)
        if self._path_suffix:
            path_suffix = set(map(int, self._path_suffix))
        else:
            path_suffix = set()

        total_paths = 0

        def dfs_counter(node: Union[int, str], path: List[Union[int, str]]) -> None:
            nonlocal total_paths
            path = list(path)
            path.append(node)
            visited.add(node)

            if len(path) >= self._path_min_len:
                if path[-1] in path_suffix or not path_suffix:
                    total_paths += 1

            if len(path) < self._path_max_len:
                for neighbor in self._neighbors[str(node)]:
                    if neighbor not in self._excluded_nodes and neighbor not in visited:
                        dfs_counter(neighbor, path)

            path.pop()
            visited.remove(node)

        if not self._path_prefix:
            for node in self._graph:
                if node not in visited:
                    dfs_counter(node, self._path_prefix)
        else:
            dfs_counter(self._path_prefix[-1], self._path_prefix[:-1])

        return total_paths

    def dfs(self) -> Tuple[bool, List]:
        visited = set(self._path_prefix)
        if self._path_suffix:
            path_suffix = set(map(int, self._path_suffix)) 
        else:
            path_suffix = set()

        def calculate_node_distance(graph, node1, node2):
            distances = {}
            for node in graph:
                distances[node] = float('inf')
            distances[node1] = 0
            queue = [node1]

            while queue:
                current_node = queue.pop(0)

                if current_node == node2:
                    return distances[current_node]

                for neighbor in graph[current_node]:
                    distance = len(graph) - graph[current_node].index(neighbor)

                    if distance not in distances:
                        distances[distance] = float('inf')

                    if distances[distance] > distances[current_node] + 1:
                        distances[distance] = distances[current_node] + 1

                    queue.append(neighbor)

            return distance

        def dfs_helper(node: Union[int, str], path: List[Union[int, str]]) -> Tuple[bool, List]:
            path = list(path)
            path.append(node)
            visited.add(node)

            if len(path) >= self._path_min_len:
                print(f"In min_path_length check")
                if path[-1] in path_suffix or not path_suffix:
                    success, _path = self.process_path(path)
                    print(
                        f"process_path in min_check returned success {success} and path {_path}")
                    if success:
                        return (success, _path

            if len(path) < self._path_max_len:
                print(f"In max_path_length check")
                print(
                    f"node {node} has neighbors {self._neighbors[str(node)]}")
                for neighbor in self._neighbors[str(node)]:
                    if neighbor not in self._excluded_nodes and neighbor not in visited:
                        # distance = calculate_node_distance(node, neighbor)
                        # if distance <= self._path_max_node_distance:
                        result = dfs_helper(neighbor, path)
                        print(f"dfs_helper returned result {result}")
                        if result[0]:
                            return result

            path.pop()
            visited.remove(node)

        if not self._path_prefix:
            for node in self._graph:
                result = dfs_helper(node, [])
                if result:
                    return result
        else:
            result = dfs_helper(self._path_prefix[-1], self._path_prefix[:-1])
            if result:
                print(f"result {result}")
                return result

        return False, []
