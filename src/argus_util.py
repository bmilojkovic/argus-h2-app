import sys
import os
from datetime import datetime
from pathlib import Path

DATA_SEPARATOR = ";;"

argus_version = "1.1.2"
argus_backend = "https://argus-h2-backend.fly.dev"
# argus_backend = "https://argus-h2-backend-test.fly.dev"

log_file = "argus_err.log"


def is_installation():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_user_data_dir():
    user_data_dir = "."
    if is_installation():
        user_data_dir = os.path.join(os.environ.get("LOCALAPPDATA"), "Argus")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
    return user_data_dir


def clean_log():
    if is_installation():
        data_dir = get_user_data_dir()
        log_file_path = os.path.join(data_dir, log_file)
        if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
            os.remove(log_file_path)


def argus_log(message):
    now = datetime.now().strftime("%H:%M:%S")
    log_message = now + " " + message + "\n"
    if sys.stdout is not None:
        sys.stdout.write(log_message)
    if is_installation():
        data_dir = get_user_data_dir()
        log_file_path = os.path.join(data_dir, log_file)
        with open(log_file_path, "a") as logf:
            logf.write(log_message)
