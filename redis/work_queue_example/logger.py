import time
import os
from datetime import datetime


def log(server_name, action):
    """
    Unified logging function for all servers
    """
    # Get the main script name
    script_name = os.path.basename(__file__)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Format the log entry
    log_entry = f"[{timestamp}] [{server_name}] [{script_name}] {action}"
    
    # Print to console
    print(log_entry)
    
    # Optional: Write to file
    with open("system_log.txt", "a") as f:
        f.write(log_entry + "\n")