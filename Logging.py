import logging
import sys

# Define a common formatter for all log levels
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s")

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            
            # Root logger configuration
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.CRITICAL)
            
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            
            root_logger.addHandler(stream_handler)
        
        return cls._instance

def get_logger(calling_function=None, log_level='error'):
    logger = logging.getLogger(calling_function)
    
    # Define a mapping from string values to corresponding logging levels
    log_level_mapping = {
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'debug': logging.DEBUG,
        'info': logging.INFO
    }
    
    # Get the corresponding logging level or default to ERROR
    level = log_level_mapping.get(log_level.lower())
    
    # Set the logging level
    logger.setLevel(level)
    
    return logger