import subprocess
import sys
import time
import csv
from datetime import datetime
from config import STDOUT_NORMAL, STDOUT_SUCCESS, STDOUT_ERROR
from render import render_path
from render import render_path_steps
from substitue import substitute
from config import attempt_delay

# Credit to https://github.com/timvisee/apbf
def try_path(path, attempt_counter):
    print(f"\nTrying path: {path} with length {len(path)}")
    render_path(path)
    render_path_steps(path) 
    substituted_path = substitute(path)
    print(f"Substituted path: {substituted_path}")

    command = ["adb", "shell", "twrp", "decrypt", f"{substituted_path}"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"failed to invoke decrypt command: {e}")
        sys.exit(1)
    
    # Parse output
    #print(f"Output: {result}")
    status = result.returncode
    stdout = result.stdout
    stderr = result.stderr
    stdout_replaced = stdout.replace('\n', '\\n')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attempt_counter += 1
    

    # Write to CSV
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, path, substituted_path, stdout_replaced, stderr])

    # Check for success
    if status == 0 and stderr == "" and stdout in STDOUT_SUCCESS:
        print(f"\nSuccess! Here is the output for the decryption attempt: {path}")
        return True

    # Regular output, continue
    if status == 0 and stderr == "" and stdout == STDOUT_NORMAL:
        print(f"Path {path} | {substituted_path} was not successful.")
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