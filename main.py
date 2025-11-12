import asyncio
from async_tkinter_loop import async_handler, async_mainloop
from argus_gui import check_twitch_connection, make_gui

import os
import subprocess

from slpp import slpp

import argus_gui_components
from argus_parsing import observer_loop

def read_save():
    save_file_path = "test" + os.sep + "Profile1_Temp.sav"
    lua_file_path = "current.lua"
    result = subprocess.run(["." + os.sep + "tools" + os.sep + "HadesSavesExtractor", "--extract", save_file_path, "--out", lua_file_path])

    try:
        with open(lua_file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{lua_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    save_data = slpp.decode("{" + content + "}")



def main():
    make_gui()

    # set up the twitch check task that we want to do in the background on startup
    check_event_loop = asyncio.new_event_loop()
    check_event_loop.create_task(check_twitch_connection())
    check_event_loop.create_task(observer_loop())
    # start the Tkinter event loop
    async_mainloop(argus_gui_components.root, check_event_loop)

if __name__ == "__main__":
    main()