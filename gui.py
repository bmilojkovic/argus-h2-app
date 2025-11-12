import tkinter as tk
from async_tkinter_loop import async_handler, async_mainloop
from tkinter import filedialog
import os

import gui_components
from argus_util import argus_log
from sysutil import get_steam_path
import argus_auth

def update_save_location(save_path):
    gui_components.save_path_entry.config(state="enabled")
    gui_components.save_path_entry.delete(0, tk.END)
    gui_components.save_path_entry.insert(0, save_path)
    gui_components.save_path_entry.config(state="disabled")

    # this file should always be in the save folder
    if os.path.isdir(save_path) and os.path.isfile(os.path.join(save_path, "GlobalSettingsWin.sjson")):
        gui_components.save_path_label.config(image = gui_components.check_icon)
    else:
        gui_components.save_path_label.config(image = gui_components.x_icon)

def browse_save_location():
    dirpath = filedialog.askdirectory(
        title="Please find the Hades II Save folder",
    )
    if dirpath:
        update_save_location(dirpath)

def check_save_location():
    default_save_location = os.path.join(os.environ["USERPROFILE"], "Saved Games", "Hades II")
    if os.path.isdir(default_save_location):
        update_save_location(default_save_location)

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

    # title
    gui_components.root.rowconfigure(0, weight=1)
    gui_components.title_label.grid(row=0, column=0, columnspan=2)

    # save path text
    gui_components.save_path_label.grid(row=1, column=0)

    # save path inputs
    gui_components.save_path_entry.grid(row=2, column=0)
    check_save_location()
    gui_components.save_path_browse_button.config(command=browse_save_location)
    gui_components.save_path_browse_button.grid(row=2, column=1)

    # empty row as a separator
    gui_components.root.rowconfigure(3, minsize=30)

    # twitch connect text
    gui_components.twitch_connect_label.grid(row=4, column=0)

    # twitch connect inputs
    gui_components.twitch_profile_label.grid(row=5, column=0)
    gui_components.twitch_connect_button.config(command=async_handler(perform_twitch_connection))
    gui_components.twitch_connect_button.grid(row=5, column=1)

    gui_components.root.after(100, check_twitch_connection_command)

    # empty row as a separator
    gui_components.root.rowconfigure(6, minsize=30)

    # info text
    gui_components.info_label.grid(row=7, column=0, columnspan=2)

    # Start the Tkinter event loop
    async_mainloop(gui_components.root)
