from abc import ABC, abstractmethod
import subprocess
import sys
import time
import os
import csv
import logging
from typing import Optional
from datetime import datetime
from Config import Config
from Logging import get_logger


class PathHandler(ABC):
    """
    Abstract class for handling paths.
    """
    
    @abstractmethod
    def handle_path(self, path) -> bool:
        pass
    
    def __init__(self):
        self.config = Config.load_config('config.yaml')
        self.logger = logging.getLogger('main') 

class ADBHandler(PathHandler):
    """
    Handles paths using ADB for decryption.
    """
    def __init__(self):
        """
        Initialize ADBHandler with configuration settings.
        """
        super().__init__()
        self.stdout_normal = self.config.stdout_normal
        self.stdout_success = self.config.stdout_success
        self.stdout_error = self.config.stdout_error
        self.attempt_delay = self.config.attempt_delay
        self.paths_log_file_path = self.config.paths_log_file_path
        self.attempted_paths = self.get_attempted_paths()
        self.timeout = self.config.adb_timeout
    
    def get_attempted_paths(self):
        """
        Retrieve paths that have already been attempted.
        """
        attempted_paths = []
        if not os.path.isfile(self.paths_log_file_path):
            self.logger.debug(f"Creating paths log file at {self.paths_log_file_path}")
            with open(self.paths_log_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'path', 'result'])
        else:
            self.logger.debug(f"Found existing paths log file at {self.paths_log_file_path}")
            with open(self.paths_log_file_path, newline='') as f:
                reader = csv.reader(f)
                if csv.Sniffer().has_header(f.read(1024)):
                    f.seek(0) 
                    next(reader) 
                try:
                    for row in reader:
                        if len(row) >= 2:  # Ensure at least two columns are present
                            attempted_paths.append(row[1])
                        else:
                            self.logger.warning('Malformed row in CSV file. Skipping.')
                except StopIteration:
                    self.logger.warning('No attempted paths found in CSV file')
            if not attempted_paths:
                self.logger.warning('No attempted paths found in CSV file')
        return tuple(attempted_paths)
    
    # Credit to https://github.com/timvisee/apbf
    def handle_path(self, path) -> (bool, Optional[str]):
        """
        Attempts to decrypt using the given path.
        """
        if path in self.attempted_paths:
            self.logger.info(f"Skipping path {path} because it was already tried.")
            return False
        self.logger.info(f"Trying path: {path} with length {len(path)}")
        formatted_path = ''.join(map(str, path))
        command = ["adb", "shell", "twrp", "decrypt", formatted_path]
        # print("Sending command: ", command)
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            # self.logger.error(f"Subprocess timed out: {e}")
            print(f"Subprocess timed out: {e}")
            sys.exit(1)
        except Exception as e:
            # self.logger.error(f"Failed to invoke decrypt command: {e}")
            print(f"Failed to invoke decrypt command: {e}")
            sys.exit(1)
        
        #Parse output
        # print(f"Output: {result}")
        status = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        stdout_replaced = stdout.replace('\n', '\\n')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Pass the response to the LogHandler
        log_handler = LogHandler()
        log_handler.handle_path(timestamp, path, result, stdout_replaced)

        # Check for success
        if status == 0 and stderr == "" and stdout in self.stdout_success:
            self.logger.info(f"\nSuccess! Here is the output for the decryption attempt: {path}")
            return (True, path)

        # Regular output, continue
        if status == 0 and stderr == "" and stdout == self.stdout_normal:
            print(f"Path {path} was not successful.")
            i = 0.1
            time_remaining = self.attempt_delay/1000
            while i <= time_remaining:
                time.sleep(i)
                time_remaining = time_remaining - i
                sys.stdout.write(f'\rContinuing in: {time_remaining:.1f} seconds  ')
                sys.stdout.flush()  # necessary for the line to be printed immediately
            return (False, None)

        # Report and exit
        print("Should not get here")
        self.logger.error("An error occurred, here's the output for the decryption attempt:")
        self.logger.error(f"- status: {status}")
        self.logger.error(f"- stdout: {stdout}")
        self.logger.error(f"- stderr: {stderr}")
        return False

class TestHandler(PathHandler):
    """
    Test handler for paths mocking decrypting against a known path.
    """
    def __init__(self):
        super().__init__()
        self.test_path = self.config.test_path
        print(f"[TEST] [CONFIGURATION] Grid size is {self.config.grid_size}")
        print(
            f"[TEST] [CONFIGURATION] Path max node distance is {self.config.path_max_node_distance}")
        print(
            f"[TEST] [CONFIGURATION] Path prefix is {self.config.path_prefix}")
        print(
            f"[TEST] [CONFIGURATION] Path suffix is {self.config.path_suffix}")
        print(
            f"[TEST] [CONFIGURATION] Path excluded nodes are {self.config.excluded_nodes}")
        print(f"[TEST] [CONFIGURATION] Test path is {self.test_path}")
        print(
            f"[TEST] [CONFIGURATION] Test path length is {len(self.test_path)}")

    def handle_path(self, path) -> bool:
        self.logger.debug(f"Received path {path}")
            
        if path == self.test_path:
            print(f"\n[TEST] Success! Here is the output for the decryption attempt: {path}")
            return True, path
        else:
            print(f"[TEST] Testing path {path} against {self.test_path} was not successful.")
            return False, None

class PrintHandler(PathHandler):
    """
    Prints paths and related information for human-reability.
    """
    def __init__(self):
        super().__init__()
        self.grid_size = self.config.grid_size
    
    def handle_path(self, path) -> bool:
        path_rows = self.render_path(path)
        steps_rows = self.render_path_steps(path)
        # Print side-by-side
        print(f"[PRINT] Current path {path}")
        for path_row, steps_row in zip(path_rows, steps_rows):
            print(f"{path_row}    {steps_row}")
        print("")
        return False, None

    def render_path(self, path):
        rows = []
        grid_size = self.grid_size
        # Create a path slug and print it
        slug = "-".join(str(p) for p in path)

        # Render the pattern grid
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                if y * grid_size + x + 1 in path:
                    row.append("●")
                else:
                    row.append("○")
            rows.append("".join(row))
        return rows

    def render_path_steps(self, path):
        rows = []
        grid_size = self.grid_size
        # Render the path steps
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                value = y * grid_size + x + 1
                if value in path:
                    row.append(f"{path.index(value) + 1}")
                else:
                    row.append("·")
            rows.append(" ".join(row))
        return rows
    
class LogHandler(PathHandler):
    """
    Logs paths and responses.
    """
    def __init__(self):
        super().__init__()
        self.paths_log_file_path = self.config.paths_log_file_path

    def handle_path(self, timestamp, path, response, info) -> bool:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.paths_log_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, path, response, info])
        return True