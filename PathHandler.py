from abc import ABC, abstractmethod
import subprocess
import sys
import time
import os
import csv
import logging
from datetime import datetime
from Config import Config

class PathHandler(ABC):
    path_handler_logger = logging.getLogger(__name__)
    path_handler_logger.setLevel(logging.DEBUG)
    path_handler_logger.addHandler(logging.StreamHandler(sys.stdout))
    
    @abstractmethod
    def handle_path(self, path) -> bool:
        pass
    
    def __init__(self):
        self.config = Config.load_config('config.yaml')

class ADBHandler(PathHandler):
    def __init__(self):
        super().__init__()
        self.stdout_normal = self.config.stdout_normal
        self.stdout_success = self.config.stdout_success
        self.stdout_error = self.config.stdout_error
        self.attempt_delay = self.config.attempt_delay
        self.log_file_path = self.config.log_file_path
        self.attempted_paths = self.get_attempted_paths()
    
    def get_attempted_paths(self):
        if not os.path.isfile(self.log_file_path):
            with open(self.log_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'path', 'result'])
        attempted_paths = []
        with open(self.log_file_path, newline='') as f:
            reader = csv.reader(f)
            if csv.Sniffer().has_header(f.read(1024)):
                f.seek(0) 
                next(reader) 
            try:
                for row in reader:
                    attempted_paths.append(row[1])
            except StopIteration:
                pass
        if not attempted_paths:
            self.path_handler_logger.warning('No attempted paths found in CSV file')
        return tuple(attempted_paths)
    
    # Credit to https://github.com/timvisee/apbf
    def handle_path(self, path) -> bool:
        if path in self.attempted_paths:
            self.path_handler_logger.info(f"Skipping path {path} because it was already tried.")
            return False
        self.path_handler_logger.info(f"Trying path: {path} with length {len(path)}")

        command = ["adb", "shell", "twrp", "decrypt", f"{path}"]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except Exception as e:
            self.path_handler_logger.error(f"Failed to invoke decrypt command: {e}")
            sys.exit(1)
        
        #Parse output
        self.path_handler_logger.info(f"Output: {result}")
        status = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        stdout_replaced = stdout.replace('\n', '\\n')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Pass the response to the LogHandler
        log_handler = LogHandler()
        log_handler.handle_path(path, timestamp, result, stdout_replaced)

        # Check for success
        if status == 0 and stderr == "" and stdout in self.stdout_success:
            self.path_handler_logger.info(f"\nSuccess! Here is the output for the decryption attempt: {path}")
            return True, None

        # Regular output, continue
        if status == 0 and stderr == "" and stdout == self.stdout_normal:
            self.path_handler_logger.warning(f"Path {path} was not successful.")
            i = 0.1
            time_remaining = self.attempt_delay/1000
            while i <= time_remaining:
                time.sleep(i)
                time_remaining = time_remaining - i
                sys.stdout.write(f'\rContinuing in: {time_remaining:.1f} seconds  ')
                sys.stdout.flush()  # necessary for the line to be printed immediately
            return False

        # Report and exit
        self.path_handler_logger.error("An error occurred, here's the output for the decryption attempt:")
        self.path_handler_logger.error(f"- status: {status}")
        self.path_handler_logger.error(f"- stdout: {stdout}")
        self.path_handler_logger.error(f"- stderr: {stderr}")
        sys.exit(1)

class TestHandler(PathHandler):
    def __init__(self):
        super().__init__()
        self.test_path = self.config.test_path

    def handle_path(self, path) -> bool:
        if path == self.test_path:
            self.path_handler_logger.info(f"\n[TEST] Success! Here is the output for the decryption attempt: {path}")
            return True
        else:
            self.path_handler_logger.info(f"[TEST] Path {path} was not successful.")
            return False

class PrintHandler(PathHandler):
    def __init__(self):
        super().__init__()
        self.grid_size = self.config.grid_size
    
    def handle_path(self, path) -> bool:
        path_rows = self.render_path(path)
        steps_rows = self.render_path_steps(path)
        # Print side-by-side
        for path_row, steps_row in zip(path_rows, steps_rows):
            self.path_handler_logger.info(f"{path_row}    {steps_row}")
        self.path_handler_logger.info("")
        return True

    def render_path(self, path):
        rows = []
        grid_size = grid_size
        # Create a path slug and print it
        slug = "-".join(str(p) for p in path)

        # Render the pattern grid
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                if y * grid_size + x in path:
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
                value = y * grid_size + x
                if value in path:
                    row.append(f"{path.index(value) + 1}")
                else:
                    row.append("·")
            rows.append(" ".join(row))
        return rows
    
class LogHandler(PathHandler):
    def __init__(self):
        super().__init__()
        self.log_file_path = self.config.log_file_path

    def handle_path(self, path, response) -> bool:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, path, response])
        return True