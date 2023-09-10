import argparse
import sys
import logging
from Config import Config
from PathFinder import PathFinder
from PathHandler import ADBHandler, PrintHandler, TestHandler, LogHandler #, iOSHandler

config = Config.load_config('config.yaml')
path_finder = PathFinder(config.grid_size, config.path_min_length, config.path_max_length, config.path_prefix, config.path_suffix, config.excluded_nodes, config.debug)

if __name__ == "__main__":
    main_logger = logging.getLogger(__name__)
    main_logger.setLevel(logging.DEBUG)
    main_logger.info(f" Starting main.py with config: {config}")

    parser = argparse.ArgumentParser(description='Please configure applicable handlers. Example: python main.py -apl')

    handler_classes = {
    'a': {'class': ADBHandler, 'help': 'Attempt decryption via ADB shell on Android device'},
    #'i': {'class': iOSHandler, 'help': 'Add iOS handler - runs path via iOS device'},
    'p': {'class': PrintHandler, 'help': 'Print attempted paths to console while running dfs'},
    't': {'class': TestHandler, 'help': 'Run mock brute force against test_path in config'},
    }

    parser.add_argument('-l', dest='log_enabled', action='store_true', default=False, help='Enable logging to log_file_path in config')

    for arg, handler_info in handler_classes.items():
        parser.add_argument(f'-{arg}', dest=arg, action='store_true', default=False, help=handler_info['help'])

    if len(sys.argv) == 1:
        main_logger.error(" At least one argument is required.")
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    for arg, handler_info in handler_classes.items():
        if getattr(args, arg):
            main_logger.debug(f" Adding handler: {handler_info['class']}")
            if args.log_enabled and handler_info['class'] == ADBHandler:
                main_logger.debug(f" Logging enabled.")
                handler_class = handler_info['class'](True, config.log_file_path)
            else:
                main_logger.debug(f" Logging disabled.")
                handler_class = handler_info['class']
            handler = handler_class()
            path_finder.add_handler(handler)
    
    main_logger.info(f" Calculating possible paths...")
    possible_paths = path_finder.total_paths    
    main_logger.info(f" Completed possible path calculation. Running handlers (args: {args}) on {possible_paths} possible paths...") 
    result = path_finder.dfs()    
    main_logger.info(f" Reached end of paths to try. Exiting.")
    if args.l:
        main_logger.info(f" See log.csv for results.")