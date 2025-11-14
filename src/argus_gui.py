import subprocess
import asyncio
import tkinter as tk
from async_tkinter_loop import async_handler
from tkinter import filedialog
import os

from argus_network import do_argus_auth, get_argus_token, check_argus_token_ok
import argus_gui_components
import argus_observing


def update_save_location(save_path):
    argus_gui_components.save_path_entry.config(state="enabled")
    argus_gui_components.save_path_entry.delete(0, tk.END)
    argus_gui_components.save_path_entry.insert(0, save_path)
    argus_gui_components.save_path_entry.config(state="disabled")

    # this file should always be in the save folder
    if os.path.isdir(save_path) and os.path.isfile(
        os.path.join(save_path, "GlobalSettingsWin.sjson")
    ):
        argus_gui_components.save_path_label.config(
            image=argus_gui_components.check_icon
        )
        argus_observing.set_save_dir_path(save_path)
    else:
        argus_gui_components.save_path_label.config(image=argus_gui_components.x_icon)
        argus_observing.unset_save_dir_path()


def browse_save_location():
    dirpath = filedialog.askdirectory(
        title="Please find the Hades II Save folder",
    )
    if dirpath:
        update_save_location(dirpath)


def check_save_location():
    default_save_location = os.path.join(
        os.environ["USERPROFILE"], "Saved Games", "Hades II"
    )
    if os.path.isdir(default_save_location):
        update_save_location(default_save_location)


def update_twitch_connection(success, argus_token, profile_pic):
    if success:
        argus_gui_components.twitch_connect_label.config(
            image=argus_gui_components.check_icon, text="Twitch Connection"
        )
        argus_gui_components.twitch_connect_button.config(text="Reconnect")
        new_icon = argus_gui_components.read_png_from_url(
            profile_pic, size=argus_gui_components.twitch_profile_label.winfo_height()
        )
        if new_icon is not None:
            argus_gui_components.twitch_profile_label.config(image=new_icon)
            # have to save a reference for garbage collection purposes
            argus_gui_components.twitch_profile_label.image = new_icon
        else:
            argus_gui_components.twitch_profile_label.config(
                image=argus_gui_components.question_icon
            )
        argus_observing.set_argus_token(argus_token)
    else:
        argus_gui_components.twitch_connect_label.config(
            image=argus_gui_components.x_icon, text="Twitch Connection"
        )
        argus_gui_components.twitch_connect_button.config(text="Connect")
        argus_observing.unset_argus_token()


async def perform_twitch_connection():
    argus_token, profile_pic = do_argus_auth()
    update_twitch_connection(argus_token is not None, argus_token, profile_pic)


async def check_twitch_connection():
    # give time to the GUI thread to finish drawing
    await asyncio.sleep(1)

    argus_token, profile_pic = get_argus_token()

    argus_gui_components.twitch_connect_button.config(state="enabled")
    if argus_token != "FAIL":
        update_twitch_connection(
            check_argus_token_ok(argus_token), argus_token, profile_pic
        )
    else:
        update_twitch_connection(False, None, None)


def check_twitch_connection_wrapper():
    # Checking if our Argus token is good might take a while, so we async it
    async_handler(check_twitch_connection)()


def setup_root():
    argus_gui_components.root.resizable(False, False)
    argus_gui_components.root.columnconfigure(0, weight=1)
    argus_gui_components.root.columnconfigure(1, weight=1)
    argus_gui_components.root.rowconfigure(0, weight=1)
    argus_gui_components.root.title("Argus")

    window_icon_image = tk.PhotoImage(file=os.path.join("img", "logo192.png"))
    argus_gui_components.root.iconphoto(True, window_icon_image)

    # title
    argus_gui_components.title_label.grid(row=0, column=0, columnspan=2)


def make_main_gui():
    # The GUI components are created in gui_components.py
    # Here we do all the GUI configuration and packing

    setup_root()

    # save path text
    argus_gui_components.save_path_label.grid(row=1, column=0)

    # save path inputs
    argus_gui_components.save_path_entry.grid(row=2, column=0)
    check_save_location()
    argus_gui_components.save_path_browse_button.config(command=browse_save_location)
    argus_gui_components.save_path_browse_button.grid(row=2, column=1)

    # empty row as a separator
    argus_gui_components.root.rowconfigure(3, minsize=30)

    # twitch connect text
    argus_gui_components.twitch_connect_label.grid(row=4, column=0)

    # twitch connect inputs
    argus_gui_components.twitch_profile_label.grid(row=5, column=0)
    argus_gui_components.twitch_connect_button.config(
        command=async_handler(perform_twitch_connection)
    )
    argus_gui_components.twitch_connect_button.grid(row=5, column=1)

    # empty row as a separator
    argus_gui_components.root.rowconfigure(6, minsize=30)

    # info text
    argus_gui_components.info_label.grid(row=7, column=0, columnspan=2)


def make_update_gui(details):
    setup_root()

    argus_gui_components.update_info_label.grid(row=1, column=0, columnspan=2)
    argus_gui_components.changelog_label.grid(row=2, column=0, columnspan=2)
    changelog_message = ""
    for changelog_line in details["changelog"]:
        changelog_message += changelog_line + "\n"
    argus_gui_components.changelog_label.config(text=changelog_message)

    argus_gui_components.update_button.grid(row=3, column=0)
    argus_gui_components.update_button.config(command=perform_update)

    argus_gui_components.update_quit_button.grid(row=3, column=1)
    argus_gui_components.update_quit_button.config(command=perform_quit)


def perform_update():
    subprocess.Popen(["updater.exe"])
    argus_gui_components.root.destroy()


def perform_quit():
    argus_gui_components.root.destroy()
