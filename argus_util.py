
import sys
from datetime import datetime

def argus_log(message):
    now = datetime.now().strftime("%H:%M:%S")
    sys.stdout.write(now + " " + message + "\n")
        