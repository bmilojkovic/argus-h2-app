import sys
import os
from datetime import datetime
from pathlib import Path

DATA_SEPARATOR = ";;"

argus_version = "1.1.0"
argus_backend = "https://argus-h2-backend.fly.dev"
# argus_backend = "https://argus-h2-backend-test.fly.dev"

log_file = "argus_err.log"


def clean_log():
    if sys.executable.endswith("argus.exe"):
        exe_path = Path(sys.executable).parent
        log_file_path = os.path.join(exe_path, log_file)
        if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
            os.remove(log_file_path)


def argus_log(message):
    now = datetime.now().strftime("%H:%M:%S")
    log_message = now + " " + message + "\n"
    if sys.stdout is not None:
        sys.stdout.write(log_message)
    if sys.executable.endswith("argus.exe"):
        exe_path = Path(sys.executable).parent
        log_file_path = os.path.join(exe_path, log_file)
        with open(log_file_path, "a") as logf:
            logf.write(log_message)
