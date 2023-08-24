from abc import ABC, abstractmethod
import subprocess
import sys
import time
import csv
from datetime import datetime
from RenderHandler import render_path
from RenderHandler import render_path_steps
from ConfigHandler import ConfigHandler

# Load config file
config = ConfigHandler('config.yaml')

# Assigning variables
stdout_normal = config.get_value('outputstrings.stdout_normal')
stdout_success = config.get_value('outputstrings.stdout_success')
stdout_error = config.get_value('outputstrings.stdout_error')
attempt_delay = config.get_value('attempt_delay')

class PathHandler(ABC):
    
    @abstractmethod
    def try_path(self, path):
        pass

class ADBHandler(PathHandler):
    def __init__(self, log_file="log.csv"):
        self.log_file = log_file

        # Credit to https://github.com/timvisee/apbf
    def try_path(self, path):
        print(f"\nTrying path: {path} with length {len(path)}")
        render_path(path)
        render_path_steps(path) 

        command = ["adb", "shell", "twrp", "decrypt", f"{path}"]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
        except Exception as e:
            print(f"failed to invoke decrypt command: {e}")
            sys.exit(1)
        
        #Parse output
        print(f"Output: {result}")
        status = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        stdout_replaced = stdout.replace('\n', '\\n')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to CSV
        with open('log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, path, stdout_replaced, stderr])

        # Check for success
        if status == 0 and stderr == "" and stdout in stdout_success:
            print(f"\nSuccess! Here is the output for the decryption attempt: {path}")
            return True

        # Regular output, continue
        if status == 0 and stderr == "" and stdout == stdout_normal:
            print(f"Path {path} was not successful.")
            i = 0.1
            time_remaining = attempt_delay/1000
            while i <= time_remaining:
                time.sleep(i)
                time_remaining = time_remaining - i
                sys.stdout.write(f'\rContinuing in: {time_remaining:.1f} seconds  ')
                sys.stdout.flush()  # necessary for the line to be printed immediately
            return False

        # Report and exit
        print("An error occurred, here's the output for the decryption attempt:")
        print(f"- status: {status}")
        print(f"- stdout: {stdout}")
        print(f"- stderr: {stderr}")
        sys.exit(1)

class DummyHandler(PathHandler):
    def __init__(self, test_path):
        self.test_path = test_path
        self.counter = 0

    def try_path(self, path):
        print(f"Found valid path: {path} with length {len(path)}")
        #render_path(path)
        #render_path_steps(path) 

        if path == self.test_path:
            print(f"\nSuccess! Here is the output for the decryption attempt: {path}")
            sys.exit()
            return True
        else:
            self.counter += 1
           # print(f"Path {path} was not successful.")
            return False, self.counter
        