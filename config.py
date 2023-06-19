# Graph represented as <node>: <its neighbours>,
# of a 5x5 grid:
#  0 - 1 - 2 - 3 - 4
#  |   |   |   |   |
#  5 - 6 - 7 - 8 - 9
#  |   |   |   |   |
#  10 11  12  13  14
#  |   |   |   |   |
#  15 16  17  18  19
#  |   |   |   |   |
#  20 21  22  23  24 

#  1 - 2 - 3 - 4 - 5
#  |   |   |   |   |
#  6 - 7 - 8 - 9 - :
#  |   |   |   |   |
#  ;   <  =    >   ?
#  |   |   |   |   |
#  @   A   B   C   D
#  |   |   |   |   |
#  E   F   G   H  I

graph = {
    0: [1, 5, 6],
    1: [0, 2, 5, 6, 7],
    2: [1, 3, 6, 7, 8],
    3: [2, 4, 7, 8, 9],
    4: [3, 8, 9],
    5: [0, 1, 6, 10, 11],
    6: [0, 1, 2, 5, 7, 10, 11, 12],
    7: [1, 2, 3, 6, 8, 11, 12, 13],
    8: [2, 3, 4, 7, 9, 12, 13, 14],
    9: [3, 4, 8, 13, 14],
    10: [5, 6, 11, 15, 16],
    11: [5, 6, 7, 10, 12, 15, 16, 17],
    12: [6, 7, 8, 11, 13, 16, 17, 18],
    13: [7, 8, 9, 12, 14, 17, 18, 19],
    14: [8, 9, 13, 18, 19],
    15: [10, 11, 16, 20, 21],
    16: [10, 11, 12, 15, 17, 20, 21, 22],
    17: [11, 12, 13, 16, 18, 21, 22, 23],
    18: [12, 13, 14, 17, 19, 22, 23, 24],
    19: [13, 14, 18, 23, 24],
    20: [15, 16, 21],
    21: [15, 16, 17, 20, 22],
    22: [16, 17, 18, 21, 23],
    23: [17, 18, 19, 22, 24],
    24: [18, 19, 23]
}

# Config
GRID_SIZE = 5
path_min_length = 5
path_max_length = 21
path_prefix = [20, 15, 10, 5, 0]
path_suffix = []
excluded_nodes = [6, 9, 16, 21]
attempt_counter = 1
attempt_delay = 10100

# Output strings
STDOUT_NORMAL = "Attempting to decrypt data partition or user data via command line.\nAttempting to decrypt FBE for user 0...\nFailed to decrypt user 0\n";
STDOUT_SUCCESS = "Data successfully decrypted"
STDOUT_ERROR = 'some_error_string'