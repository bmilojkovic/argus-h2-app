import sys
from datetime import datetime

DATA_SEPARATOR = ";;"

argus_version = "1.1.0"
# argus_backend = "https://argus-h2-backend.fly.dev"
argus_backend = "https://argus-h2-backend-test.fly.dev"


def argus_log(message):
    now = datetime.now().strftime("%H:%M:%S")
    sys.stdout.write(now + " " + message + "\n")
