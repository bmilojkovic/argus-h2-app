import tkinter as tk
from async_tkinter_loop import async_handler, async_mainloop
from tkinter import filedialog
import os

import gui_components
from argus_util import argus_log
from sysutil import get_steam_path
import argus_auth

def update_game_location(game_path):
    if os.path.isdir(game_path):
        gui_components.game_path_entry.config(state="enabled")
        gui_components.game_path_entry.delete(0, tk.END)
        gui_components.game_path_entry.insert(0, game_path)
        gui_components.game_path_entry.config(state="disabled")
        gui_components.game_path_label.config(image = gui_components.check_icon)

def browse_game_location():
    dirpath = filedialog.askdirectory(
        title="Please find the Hades II folder",
    )
    if dirpath and os.path.basename(dirpath) == "Hades II":
        update_game_location(dirpath)

def check_steam_location():
    steam_path = get_steam_path()
    if steam_path != None:
        game_path = steam_path + os.sep + "steamapps" + os.sep + "common" + os.sep + "Hades II"
        update_game_location(game_path)

def update_twitch_connection(success, profile_pic):
    if success:
        gui_components.twitch_connect_label.config(image=gui_components.check_icon, text="Twitch Connection")
        gui_components.twitch_connect_button.config(text="Reconnect")
        new_icon = gui_components.read_png_from_url(profile_pic, size=gui_components.twitch_profile_label.winfo_height())
        if new_icon != None:
            gui_components.twitch_profile_label.config(image=new_icon)
            # have to save a reference for garbage collection purposes
            gui_components.twitch_profile_label.image = new_icon
        else:
            gui_components.twitch_profile_label.config(image=gui_components.question_icon)
    else:
        gui_components.twitch_connect_label.config(image=gui_components.x_icon, text="Twitch Connection")
        gui_components.twitch_connect_button.config(text="Connect")

async def perform_twitch_connection():
    argus_token, profile_pic = argus_auth.do_argus_auth()
    update_twitch_connection(argus_token != None, profile_pic)

async def check_twitch_connection():
    argus_token, profile_pic = argus_auth.get_argus_token()

    gui_components.twitch_connect_button.config(state="enabled")
    if argus_token != "FAIL":
        update_twitch_connection(argus_auth.check_argus_token_ok(argus_token), profile_pic)
    else:
        update_twitch_connection(False, None)
        
def check_twitch_connection_command():
    # Checking if our Argus token is good might take a while, so we async it
    async_handler(check_twitch_connection)()

def make_gui():
    # The GUI components are created in gui_components.py
    # Here we do all the GUI configuration and packing

    #gui_components.root.rowconfigure(0, weight=1)
    gui_components.root.columnconfigure(0, weight=1)
    gui_components.root.columnconfigure(1, weight=1)

    gui_components.root.title("Argus")

    window_icon_image = tk.PhotoImage(file='logo192.png')
    gui_components.root.iconphoto(True, window_icon_image)

    gui_components.game_path_label.grid(row=0, column=0)
    gui_components.game_path_entry.grid(row=1, column=0)
    
    check_steam_location()

    gui_components.game_path_browse_button.config(command=browse_game_location)
    gui_components.game_path_browse_button.grid(row=1, column=1)

    gui_components.twitch_connect_label.grid(row=2, column=0)
    gui_components.twitch_profile_label.grid(row=3, column=0)

    gui_components.twitch_connect_button.config(command=async_handler(perform_twitch_connection))
    gui_components.twitch_connect_button.grid(row=3, column=1)

    gui_components.root.after(100, check_twitch_connection_command)

    # Start the Tkinter event loop
    async_mainloop(gui_components.root)
