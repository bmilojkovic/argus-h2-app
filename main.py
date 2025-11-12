from async_tkinter_loop import async_handler
from gui import check_twitch_connection, make_gui

import os
import subprocess

from slpp import slpp

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

if __name__ == "__main__":
    main()