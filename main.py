import argparse
import sys
from Logging import Logger, get_logger  # Import the Logger class and get_logger function
from Config import Config
from PathFinder import PathFinder
from PathHandler import ADBHandler, PrintHandler, TestHandler, LogHandler #, iOSHandler

config = Config.load_config('config.yaml')
path_finder = PathFinder(config.grid_size, config.path_min_length, config.path_max_length,
                         config.path_max_node_distance, config.path_prefix, config.path_suffix, config.excluded_nodes)

def validate_mode(value):
    # Extract valid modes from the handler_classes keys
    valid_modes = ''.join(handler_classes.keys())
    if not set(value).issubset(set(valid_modes)):
        # Create a string of available options
        available_options = ', '.join(valid_modes)
        raise argparse.ArgumentTypeError(
            f"Invalid mode: {value}. Allowed values are combinations of {available_options}.")
    return value

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(
        description='Please configure applicable handlers. Example: python3 main.py -m ap -l w')
    
    handler_classes = {
    'a': {'class': ADBHandler, 'help': 'Attempt decryption via ADB shell on Android device'},
    #'i': {'class': iOSHandler, 'help': 'Add iOS handler - runs path via iOS device'},
    'p': {'class': PrintHandler, 'help': 'Print attempted paths to console while running brute force'},
    't': {'class': TestHandler, 'help': 'Run mock brute force against test_path in config'},
    }

    mode_help = "Select modes: "
    for arg, handler_info in handler_classes.items():
        mode_help += f"{arg} ({handler_info['help']}), "
    
    mode_help = mode_help.rstrip(", ")  # Remove trailing comma and space

    parser.add_argument('-m', '--mode', type=validate_mode, required=True, help=mode_help)
    parser.add_argument('-l', '--logging', choices=['error', 'warning', 'debug', 'info'], default='error', help='Set logging level: e for error, w for warnings, d for debug, i for info. Critical errors will always be shown. Default is \'error\'')
    parser.add_argument('--file', action='store_true', default=False, help='Enable logging to file')

    try:
        args = parser.parse_args()
    except SystemExit:
        # Extract the valid modes as a string
        valid_modes = ', '.join(handler_classes.keys())
        # print(
        #    f"Error: Missing required '-m/--mode' argument. Allowed values are combinations of: {valid_modes}.")
        # parser.print_help()  # Print the default help message
        sys.exit(1)

    logger = get_logger('main', log_level=args.logging)
    modes = args.mode

    for mode in modes:
        if mode in handler_classes:
            handler_info = handler_classes[mode]
            handler_class = handler_info['class']
            handler = handler_class()
            path_finder.add_handler(handler)
        else:
            print(
                f"Warning: Mode '{mode}' is not recognized and will be ignored.")

    # print(f" Starting main.py with config: {config}")
    print(f"Calculating possible paths...")
    possible_paths = path_finder.total_paths
    handler_names_str = ', '.join([handler_info['class'].__name__ for arg, handler_info in handler_classes.items() if arg in args.mode])
    print(
        f"Completed. Attempting brute force with {possible_paths} possible paths via {handler_names_str}.")
    result = path_finder.dfs()
    if not result:
        print(f"Reached end of paths to try. Check path_logs.csv for more information. Exiting.")
    else:
        print(f"Success! The path is: {result}")
