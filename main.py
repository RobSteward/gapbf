import argparse
import sys
import logging
from Config import Config
from PathFinder import PathFinder
from PathHandler import ADBHandler, PrintHandler, TestHandler, LogHandler #, iOSHandler

config = Config.load_config('config.yaml')
path_finder = PathFinder(config.grid_size, config.path_min_length, config.path_max_length, config.path_prefix, config.path_suffix, config.excluded_nodes, config.debug)

def set_logger_level(args, logger):
    """
    Set logger level based on command-line arguments.
    
    Parameters:
        args: Parsed command-line arguments.
        logger: Logger instance.
    """
    log_levels = {
        'w': logging.WARNING,
        'd': logging.DEBUG,
        'v': logging.INFO,
        'e': logging.ERROR,  # Default case
    }

    logger.setLevel(log_levels.get(args.logging, logging.ERROR))
    
    # Add a console handler to the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_levels.get(args.logging, logging.ERROR))
    logger.addHandler(console_handler)
    
    logger.info(f"Logging level set to {logging.getLevelName(logger.level)}.")

def validate_mode(value):
    valid_modes = set('apt')
    if not set(value).issubset(valid_modes):
        raise argparse.ArgumentTypeError(f"Invalid mode: {value}. Allowed values are combinations of 'a', 'p', and 't'.")
    return value
  
 
if __name__ == "__main__":
    main_logger = logging.getLogger(__name__)
    main_logger.setLevel(logging.ERROR)
    
    parser = argparse.ArgumentParser(description='Please configure applicable handlers. Example: python main.py -m ap -l w')
    
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
    parser.add_argument('-l', '--logging', choices=['w', 'd', 'v'], default='e', help='Set logging level: w for warnings, d for debug, v for verbose')
    parser.add_argument('--file', action='store_true', default=False, help='Enable logging to file')

    args = parser.parse_args() 
    
    if not args.mode:
        main_logger.error("At least one target argument (a, p, or t) is required.")
        parser.print_help()
        sys.exit(1)
        
    set_logger_level(args, main_logger)

    for arg, handler_info in handler_classes.items():
        if arg in args.mode:  # Changed from getattr(args, arg)
            handler_class = handler_info['class']
            handler = handler_class()
            path_finder.add_handler(handler)

    main_logger.info(f" Starting main.py with config: {config}")
    main_logger.info(f" Calculating possible paths...")
    possible_paths = path_finder.total_paths
    handler_names_str = ', '.join([handler_info['class'].__name__ for arg, handler_info in handler_classes.items() if arg in args.mode])
    main_logger.info(f" Completed possible path calculation. Attempting brute force with {possible_paths} possible paths via {handler_names_str}.")
    result = path_finder.dfs()    
    main_logger.info(f" Reached end of paths to try. Exiting.")