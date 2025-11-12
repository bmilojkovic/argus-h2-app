
import asyncio
import os

from argus_util import argus_log

observer_running = True

save_file_path_good = False
argus_token_good = False

save_file_path = ""
save_dir_state = {}
argus_token = ""

def set_save_file_path(new_save_file_path):
    global save_file_path, save_file_path_good

    save_file_path = new_save_file_path
    save_file_path_good = True

    init_save_dir()

def unset_save_file_path():
    global save_file_path_good, save_dir_state

    save_file_path_good = False
    save_dir_state = {}

def set_argus_token(new_argus_token):
    global argus_token, argus_token_good

    argus_token = new_argus_token
    argus_token_good = True

def unset_argus_token():
    global argus_token_good

    argus_token_good = False

def init_save_dir():
    global save_dir_state

    try:
        with os.scandir(save_file_path) as entries:
            for entry in entries:
                if entry.name.endswith("_Temp.sav"):
                    timestamp = entry.stat().st_mtime
                    save_dir_state[entry.name] = timestamp
    except FileNotFoundError:
        argus_log(f"Error: Directory not found at '{save_file_path}'")
    except PermissionError:
        argus_log(f"Error: Permission denied to access '{save_file_path}'")

def find_newest_changed_save():
    global save_dir_state

    newest_time = 0
    newest_file = ""
    try:
        with os.scandir(save_file_path) as entries:
            for entry in entries:
                if entry.name.endswith("_Temp.sav"):
                    # Get the last modified timestamp (float representing seconds since the epoch)
                    timestamp = entry.stat().st_mtime
                    #argus_log(f"Found {entry.name} with timestamp {timestamp}")
                    if entry.name not in save_dir_state:
                        # first time we see a new temp file, we just add it
                        save_dir_state[entry.name] = timestamp
                    elif save_dir_state[entry.name] < timestamp:
                        # next time, we consider it a candidate as long as it updated
                        save_dir_state[entry.name] = timestamp
                        if timestamp > newest_time:
                            newest_time = timestamp
                            newest_file = entry.name
    except FileNotFoundError:
        argus_log(f"Error: Directory not found at '{save_file_path}'")
    except PermissionError:
        argus_log(f"Error: Permission denied to access '{save_file_path}'")

    if newest_time != 0:
        return newest_file
    
    return None

async def observer_loop():
    # give the GUI thread a bit of breathing room on start
    await asyncio.sleep(1)
    while observer_running:
        if save_file_path_good and argus_token_good:
            newest_changed_save = find_newest_changed_save()
            if newest_changed_save != None:
                argus_log("Sending data for savefile " + os.path.join(save_file_path, newest_changed_save))
        await asyncio.sleep(1)