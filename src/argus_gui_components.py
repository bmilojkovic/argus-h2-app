import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pytablericons import TablerIcons, OutlineIcon
import requests
from io import BytesIO

from argus_util import argus_log


def read_png_from_url(url, size):
    """
    Reads a PNG image from a given URL and returns a Pillow Image object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Open the image from the in-memory bytes
        img = Image.open(BytesIO(response.content))

        # Ensure it's a PNG, or handle other formats if needed
        if img.format != "PNG":
            argus_log(
                f"Warning: Image at {url} is not a PNG, but a {img.format}. Attempting to process anyway."
            )

        img = img.resize([size, size])

        return ImageTk.PhotoImage(img)
    except requests.exceptions.RequestException as e:
        argus_log(f"Error downloading image from {url}: {e}")
        return None
    except Image.UnidentifiedImageError:
        argus_log(
            f"Error: Cannot identify image file from {url}. It might not be a valid image or the format is unsupported."
        )
        return None
    except Exception as e:
        argus_log(f"An unexpected error occurred: {e}")
        return None


def get_tabler_icon_as_tk_image(icon_enum, size=24, color="#000000", stroke_width=2.0):
    """Loads a Tabler Icon and returns it as a Tkinter PhotoImage."""
    icon_data = TablerIcons.load(
        icon_enum, size=size, color=color, stroke_width=stroke_width
    )

    return ImageTk.PhotoImage(icon_data)


root = tk.Tk()
root.configure(bg="white")
check_icon = get_tabler_icon_as_tk_image(OutlineIcon.CHECK, size=32, color="#28a745")
x_icon = get_tabler_icon_as_tk_image(OutlineIcon.X, size=32, color="#b51233")
question_icon = get_tabler_icon_as_tk_image(
    OutlineIcon.QUESTION_MARK, size=32, color="#000000"
)
info_icon = get_tabler_icon_as_tk_image(
    OutlineIcon.INFO_CIRCLE, size=32, color="#000000"
)
title_label = ttk.Label(
    root, text="Argus 👀", font=("Helvetica", 28, "bold"), background="white"
)
save_path_label = ttk.Label(
    root,
    image=x_icon,
    font=("Helvetica", 16),
    text="Hades II Save Location",
    compound=tk.RIGHT,
    background="white",
)

save_path_entry = ttk.Entry(root, width=40, state="disabled")
save_path_browse_button = ttk.Button(root, text="Browse")

twitch_connect_label = ttk.Label(
    root,
    image=question_icon,
    font=("Helvetica", 16),
    text="Twitch Connection: Checking...",
    compound=tk.RIGHT,
    background="white",
)
twitch_profile_label = ttk.Label(root, image=question_icon, background="white")
twitch_connect_button = ttk.Button(root, text="Connect", state="disabled")
info_label = ttk.Label(
    root,
    image=info_icon,
    font=("Helvetica", 10),
    text="Both checks need to be passing ✅ for the extension to work.\nLeave this app running in the background while streaming.",
    compound=tk.LEFT,
    background="white",
)

# update UI
update_info_label = ttk.Label(
    root,
    image=info_icon,
    font=("Helvetica", 10),
    text=(
        "An important update for Argus is available.\n"
        + "Please download it from our release page\n"
        + "and install it before proceeding.\n"
        + "Here are all the changes:"
    ),
    compound=tk.LEFT,
    background="white",
)
changelog_label = ttk.Label(root, font=("Helvetica", 16), background="white")
update_button = ttk.Button(root, text="Update")
update_quit_button = ttk.Button(root, text="Quit")

# timeout UI
timeout_label = ttk.Label(
    root,
    text="There seems to be an issue with our sevice. :(\nWe are sorry for the inconvenience. Please try again later.",
    font=("Helvetica", 16),
    background="white",
)
