from abc import ABC, abstractmethod
import subprocess
import sys
import time
import os
import csv
import logging
from datetime import datetime

command = ["adb", "shell", "twrp", "decrypt", "145"]
print(command)
timeout = 10

try:
    result = subprocess.run(command, capture_output=True,
                            text=True, timeout=timeout)
except subprocess.TimeoutExpired as e:
    logging.error(f"Subprocess timed out: {e}")
    sys.exit(1)
except Exception as e:
    logging.error(f"Failed to invoke decrypt command: {e}")
    sys.exit(1)
