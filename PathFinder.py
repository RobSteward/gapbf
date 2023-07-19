from PathHandler import PathHandler    
    
    # Depth-first search recursive traversal of the graph,
    #  # which calls path_handler function on each path.
    # You can also specify the prefix from which to start
    # and the maximum path length.
class PathFinder:
    def __init__(self, graph_size):
        self.graph_size = graph_size
        self.graphs = {
            "3x3": {
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
            "4x4": {
                "graph": [1,2,3,4,5,6,7,8,9,:,;,<,=,>,?,@],
                "neighbors": {
                "1": [2, 5, 6], 
                "2": [1, 3, 5, 6, 7],
                "3": [2, 4, 6, 7, 8],
                "4": [3, 7, 8],
                "5": [1, 2, 6, 9, :],
                "6": [1, 2, 3, 5, 7, 9, :, ;],
                "7": [2, 3, 4, 6, 8, :, ;, <],
                "8": [3, 4, 7, ;, <],
                "9": [5, 6, :, =, >],
                ":": [5, 6, 7, 9, ;, =, >, \?],
                ";": [6, 7, 8, :, =, >, \?, @],
                "<": [7, 8, ;, \?, @],
                "=": [9, :, >],
                ">": [9, :, ;, =, \?],
                "?": [:, ;, <, >, @],
                "@": [;, <, \?,]
                }
            },
            "5x5": {
                "graph": [1,2,3,4,5,6,7,8,9,:,;,<,=,>,?,@,A,B,C,D,E,F,G,H,I],
                "neighbors": {
                    "1": [2, 6, 7], 
                    "2": [1, 3, 6, 7, 8],
                    "3": [2, 4, 7, 8, 9],
                    "4": [3, 5, 8, 9, :],
                    "5": [4, 9, :],
                    "6": [1, 2, 7, ;, <],
                    "7": [1, 2, 3, 6, 8, ;, <, =],
                    "8": [2, 3, 4, 7, 9, <, =, >],
                    "9": [3, 4, 5, 8, :, =, >, ??],
                    ":": [4, 5, 9, >, ??],
                    ";": [6, 7, <, @, A],
                    "<": [6, 7, 8, ;, =, @, A, B],
                    "=": [7, 8, 9, <, >, A, B, C],
                    ">": [8, 9, :, =, ??, B, C, D],
                    "?": [9, :, >, C, D],
                    "@": [;, <, A, E, F],
                    "A": [;, <, =, @, B, E, F, G],
                    "B": [<, =, >, A, C, F, G, H],
                    "C": [=, >, ?, B, D, G, H, I],
                    "D": [>, ?, C, H, I],
                    "E": [@, A, F],
                    "F": [@, A, B, E, G],
                    "G": [A, B, C, F, H],
                    "H": [B, C, D, G, I],
                    "I": [C, D, H]
                }
            },
            "6x6": {
                "graph": [1,2,3,4,5,6,7,8,9,:,;,<,=,>,?,@,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T],
                "neighbors": {
                    "1": [2, 7, 8],
                    "2": [1, 3, 7, 8, 9],
                    "3": [2, 4, 8, 9, :],
                    "4": [3, 5, 9, :, ;],
                    "5": [4, 6, :, ;, <],
                    "6": [5, ;, <],

                    "7": [1, 2, 8, A, B],
                    "8": [1, 2, 3, 7, 9, A, B, C],
                    "9": [2, 3, 4, 8, :, B, C, D],
                    ":": [3, 4, 5, 9, ;, C, D, E],
                    ";": [4, 5, 6, :, <, D, E, F],
                    "<": [5, 6, ;, E, F],
                    "=": [7, 8, 9, A, B, C, G, H],
                    ">": [8, 9, :, B, C, D, H, I],
                    "?": [9, :, ;, C, D, E, I, J],
                    "@": [A, B, C, G, H, I, K, L],
                    "A": [7, 8, 9, B, C, D, G, H, I, J, K, L],
                    "B": [7, 8, 9, :, A, C, D, E, G, H, I, J, K, L, M, N],
                    "C": [8, 9, :, ;, A, B, D, E, F, H, I, J, K, L, M, N, O, P],
                    "D": [9, :, ;, <, B, C, E, F, I, J, K, L, M, N, O, P, Q, R],
                    "E": [;, <, :, =, C, D, F, J, K, L, M, N, O, P, Q, R, S, T],
                    "F": [<, :, =, D, E, K, L, M, N, O, P, Q, R, S, T],
                    "G": [A, B, C, H, M, N, O],
                    "H": [A, B, C, D, G, I, M, N, O, P, Q],
                    "I": [B, C, D, E, H, J, N, O, P, Q, R],
                    "J": [C, D, E, F, I, K, O, P, Q, R, S],
                    "K": [D, E, F, J, L, P, Q, R, S, T],
                    "L": [E, F, K, Q, R, S, T],
                    "M": [G, H, I, N, O],
                    "N": [G, H, I, J, M, O, P],
                    "O": [H, I, J, K, N, P, Q],
                    "P": [I, J, K, L, O, Q, R],
                    "Q": [J, K, L, P, R, S],
                    "R": [K, L, Q, S, T],
                    "S": [L, Q, R, T],
                    "T": [Q, R, S]
                }
            },
        },
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