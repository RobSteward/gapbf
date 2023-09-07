from PathFinder import PathFinder
from PathHandler import DummyHandler
from PathHandler import ADBHandler
from Config import Config
import argparse

# Load config file
config = Config('config.yaml')
path_finder = PathFinder(config)

# Run main program
if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='PathFinder')
    parser.add_argument('a', type=bool, default=false, help='Add Android ADB handler')
    #parser.add_argument('i', type=bool, default=false, help='Add iOS handler')
    parser.add_argument('d', type=bool, default=false, help='Add dummy handler')
    parser.add_argument('l', type=bool, default=false, help='Add log handler')
    parser.add_argument('p', type=bool, default=false, help='Add print handler')
    args = parser.parse_args()

    # based on flags add handlers
    if args.a:
        adb_handler = ADBHandler(config)
        path_finder.add_handler(adb_handler)
    #if args.i:
    #    path_finder.add_handler(ios_handler)
    if args.d:
        dummy_handler = DummyHandler(config)
        path_finder.add_handler(dummy_handler)
    if args.l:
        log_handler = LogHandler(config)
        path_finder.add_handler(log_handler)
    if args.p:
        print_handler = PrintHandler(config)
        path_finder.add_handler(print_handler)
    
    print(f"\nCalculating possible paths...")
    
    # Count possible paths
    possible_paths = path_finder.count_possible_paths()
    
    print(f"Completed. Running handlers (args: {args}) on {possible_paths} possible paths...") 

    path_finder.dfs()
    
    print(f"Reached end of paths to try. Exiting. See log.csv for results.")