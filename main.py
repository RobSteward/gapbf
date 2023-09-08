import argparse
import sys
from Config import Config
from PathFinder import PathFinder
from PathHandler import DummyHandler, ADBHandler, LogHandler, PrintHandler

config = Config.load_config('config.yaml')
path_finder = PathFinder(config.grid_size, config.path_min_length, config.path_max_length, config.path_prefix, config.path_suffix, config.excluded_nodes)

if __name__ == "__main__":

    handler_classes = {
    'a': {'class': ADBHandler, 'help': 'Add Android ADB handler - runs path via ADB shell on Android device'},
    #'i': {'class': IOSHandler, 'help': 'Add iOS handler - runs path via iOS device'},
    'd': {'class': DummyHandler, 'help': 'Add dummy handler - does nothing'},
    'l': {'class': LogHandler, 'help': 'Add log handler - writes attempted paths to log.csv at passed file path'},
    'p': {'class': PrintHandler, 'help': 'Add print handler - prints attempted paths to console'}
    }

    parser = argparse.ArgumentParser(description='Configure applicable handlers: a - Android ADB, i - iOS, d - dummy, l - log, p - print. Example: python main.py a d l p')

    for arg, handler_info in handler_classes.items():
        parser.add_argument(f'-{arg}', dest=arg, action='store_true', default=False, help=handler_info['help'])

    if len(sys.argv) == 1:
        print("Error: At least one argument is required.")
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    for arg, handler_info in handler_classes.items():
        if getattr(args, arg):
            handler = handler_info['class'](config)
            path_finder.add_handler(handler)
        args = parser.parse_args()
    
    print(f"\nCalculating possible paths...")
    possible_paths = path_finder.total_paths    
    print(f"Completed. Running handlers (args: {args}) on {possible_paths} possible paths...") 
    result = path_finder.dfs()    
    print(f"Reached end of paths to try. Exiting. See log.csv for results.")