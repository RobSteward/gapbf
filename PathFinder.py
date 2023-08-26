from typing import List, Union, Set
from PathHandler import PathHandler    
    # See https://twrp.me/faq/openrecoveryscript.html
    # Define a dictionary with the substitutions

class PathFinder:
    graphs: dict =  {
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

    def __init__(self, graph_size: int):
        #print(f"Debug: Type of self.graphs: {type(self.graphs)}, Value: {self.graphs}")
        if graph_size not in self.graphs:
            raise ValueError(f'Invalid graph_size: {graph_size}. Available sizes are: {list(self.graphs.keys())}')
        
        self.graph_size = graph_size
        graph_data = self.graphs.get(self.graph_size, {})
        self.graph = graph_data.get("graph", [])
        self.neighbors = graph_data.get("neighbors", {})
        self.__handlers = []

    @property
    def handlers(self):
        return self.__handlers

    def add_handler(self, handler: PathHandler) -> None:
        if not isinstance(handler, PathHandler):
            raise TypeError("Expected a PathHandler instance.")
        self.__handlers.append(handler)
        
    def count_possible_paths(self, path_min_len: int = 4,
                             path_max_len: int = 36,
                             path_prefix: List[Union[int, str]] = [],
                             path_suffix: Set[Union[int, str]] = [],
                             excluded_nodes: Set[Union[int, str]] = []) -> int:
        """
        Count the number of possible paths based on the given configuration.
        """
        visited = set(path_prefix)
        path_suffix = set(map(int, path_suffix))  # Convert once
        counter = 0

        def dfs_counter(node: Union[int, str], path: List[Union[int, str]]) -> None:
            nonlocal counter
            path = list(path)
            path.append(node)
            visited.add(node)

            if len(path) >= path_min_len:
                if path[-1] in path_suffix or not path_suffix:
                    counter += 1

            if len(path) < path_max_len:
                for neighbor in self.neighbors[str(node)]:
                    if neighbor not in excluded_nodes and neighbor not in visited:
                        dfs_counter(neighbor, path)

            path.pop()
            visited.remove(node)

        if not path_prefix:
            for node in self.graph:
                if node not in visited:
                    dfs_counter(node, path_prefix)
        else:
            dfs_counter(path_prefix[-1], path_prefix[:-1])

        return counter

    # Depth-first search recursive traversal of the graph,
    def dfs(self, path_min_len: int = 4,
            path_max_len: int = 36,
            path_prefix: List[Union[int, str]] = [],
            path_suffix: Set[Union[int, str]] = [],
            excluded_nodes:  Set[Union[int, str]] = []) -> None:
        """
        Depth-first search recursive traversal of the graph.
        """
        visited = set(path_prefix)
        path_suffix = set(map(int, path_suffix))  # Convert once

        def dfs_helper(node: Union[int, str], path: List[Union[int, str]]) -> None:
            path = list(path)
            path.append(node)
            visited.add(node)

            if len(path) >= path_min_len:
                if path[-1] in path_suffix or not path_suffix:
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

    