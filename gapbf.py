import itertools as it
import networkx as nx
import time
import configparser
import ast

# Create grid graph
def create_grid_graph(X, Y):
    G = nx.grid_2d_graph(X, Y)
    # Add diagonal edges
    for (u, v) in G.nodes():
        if (u+1 < X and v+1 < Y):
            G.add_edge((u, v), (u+1, v+1))
        if (u+1 < X and v-1 >= 0):
            G.add_edge((u, v), (u+1, v-1))
    return G

# Convert 2D coordinates to node id
def to_node_id(coord, X):
    return coord[0] * X + coord[1]

# Convert node id to 2D coordinates
def to_2d_coord(node_id, X):
    return node_id // X, node_id % X

# Check if the path distance is within the given limit
def check_distance(path, maxDistance, X):
    for i in range(len(path) - 1):
        coord1 = to_2d_coord(path[i][0], X)
        coord2 = to_2d_coord(path[i+1][0], X)
        dist = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
        if dist > maxDistance:
            return False
    return True

# DFS for all possible paths with conditions
def dfs_paths(graph, X, maxDistance, minLength, maxLength, excluded, fixed):
    paths = []
    start_time = time.time()
    nodes = list(graph.nodes())
    for path_len in range(minLength, maxLength + 1):
        for path in it.permutations(nodes, path_len):
            if all(node not in excluded for node in path) and len(set(path)) == len(path):
                if check_distance(path, maxDistance, X):
                    paths.append([to_node_id(coord, X) for coord in path])
        paths = [path for path in paths if all(node not in excluded for node in path)]
    end_time = time.time()
    print("Time to calculate all paths: ", end_time - start_time)
    print("Number of total valid paths matching all criteria: ", len(paths))
    #for path in paths:
    #    print(path)

# Main function
def main():

    # Load configuration from file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Read settings from the configuration
    gridSizeX = config.getint('grid', 'gridSizeX')
    gridSizeY = config.getint('grid', 'gridSizeY')
    maxDistance = config.getint('path', 'maxDistance')
    minLength = config.getint('path', 'minLength')
    maxLength = config.getint('path', 'maxLength')
    excluded = config.get('excludedNodes', 'nodes').split(',')
    fixed = ast.literal_eval(config.get('fixedNodes', 'nodes'))

    # Create grid graph
    G = create_grid_graph(gridSizeX, gridSizeY)

    # Calculate all paths
    dfs_paths(G, gridSizeX, maxDistance, minLength, maxLength, excluded, fixed)

if __name__ == "__main__":
    main()