import asyncio
import os
import subprocess
from pathlib import Path
import sys

from slpp import slpp

from argus_network import send_run_data
from argus_parsing import parse_data
from argus_util import argus_log

observer_running = True

save_dir_path_good = False
argus_token_good = False

save_dir_path = ""
save_dir_state = {}
argus_token = ""


def set_save_dir_path(new_save_dir_path):
    global save_dir_path, save_dir_path_good

    save_dir_path = new_save_dir_path
    save_dir_path_good = True

    init_save_dir()


def unset_save_dir_path():
    global save_dir_path_good, save_dir_state

    save_dir_path_good = False
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
        with os.scandir(save_dir_path) as entries:
            for entry in entries:
                if entry.name.endswith("_Temp.sav"):
                    timestamp = entry.stat().st_mtime
                    save_dir_state[entry.name] = timestamp
    except FileNotFoundError:
        argus_log(f"Error: Directory not found at '{save_dir_path}'")
    except PermissionError:
        argus_log(f"Error: Permission denied to access '{save_dir_path}'")


def find_newest_changed_save():
    global save_dir_state

    newest_time = 0
    newest_file = ""
    try:
        with os.scandir(save_dir_path) as entries:
            for entry in entries:
                if entry.name.endswith("_Temp.sav"):
                    # Get the last modified timestamp (float representing seconds since the epoch)
                    timestamp = entry.stat().st_mtime
                    # argus_log(f"Found {entry.name} with timestamp {timestamp}")
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
        argus_log(f"Error: Directory not found at '{save_dir_path}'")
    except PermissionError:
        argus_log(f"Error: Permission denied to access '{save_dir_path}'")

    if newest_time != 0:
        return newest_file

    return None


def read_save_file(save_file_path):
    working_path = "."
    if sys.executable.endswith("argus.exe"):
        working_path = Path(sys.executable).parent
    lua_file_path = os.path.join(working_path, "current.lua")
    try:
        subprocess.Popen(
            [
                os.path.join(working_path, "tools", "HadesSavesExtractor.exe"),
                "--extract",
                save_file_path,
                "--out",
                lua_file_path,
            ],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
        )
    except FileNotFoundError:
        argus_log("Problem starting save extractor. Aborting.")
        return "INVALID"

    try:
        with open(lua_file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        argus_log(f"Error: The file '{lua_file_path}' was not found.")
        return "INVALID"
    except Exception as e:
        argus_log(f"An error occurred while reading lua: {e}")
        return "INVALID"

    save_data = slpp.decode("{" + content + "}")

    return parse_data(save_data["LUA_DATA"])


async def observer_loop():
    # give the GUI thread a bit of breathing room on start
    await asyncio.sleep(1)
    while observer_running:
        if save_dir_path_good and argus_token_good:
            newest_changed_save = find_newest_changed_save()
            if newest_changed_save is not None:
                save_file_path = os.path.join(save_dir_path, newest_changed_save)
                argus_log("Sending data for savefile " + save_file_path)
                argus_data = read_save_file(save_file_path)
                if argus_data == "INVALID":
                    argus_log("Skipping cycle")
                else:
                    send_run_data(argus_data)

        await asyncio.sleep(1)
