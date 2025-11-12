
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
        if img.format != 'PNG':
            argus_log(f"Warning: Image at {url} is not a PNG, but a {img.format}. Attempting to process anyway.")
        
        img = img.resize([size, size])

        return ImageTk.PhotoImage(img)
    except requests.exceptions.RequestException as e:
        argus_log(f"Error downloading image from {url}: {e}")
        return None
    except Image.UnidentifiedImageError:
        argus_log(f"Error: Cannot identify image file from {url}. It might not be a valid image or the format is unsupported.")
        return None
    except Exception as e:
        argus_log(f"An unexpected error occurred: {e}")
        return None

def get_tabler_icon_as_tk_image(icon_enum, size=24, color='#000000', stroke_width=2.0):
    """Loads a Tabler Icon and returns it as a Tkinter PhotoImage."""
    icon_data = TablerIcons.load(icon_enum, size=size, color=color, stroke_width=stroke_width)

    return ImageTk.PhotoImage(icon_data)

root = tk.Tk()
check_icon = get_tabler_icon_as_tk_image(OutlineIcon.CHECK, size=32, color='#28a745')
x_icon = get_tabler_icon_as_tk_image(OutlineIcon.X, size=32, color="#b51233")
question_icon = get_tabler_icon_as_tk_image(OutlineIcon.QUESTION_MARK, size=32, color="#000000")
info_icon = get_tabler_icon_as_tk_image(OutlineIcon.INFO_CIRCLE, size=32, color="#000000")
title_label = ttk.Label(root, text="Argus 👀", font=("Helvetica", 28, "bold")) 
save_path_label = ttk.Label(root, 
                            image=x_icon, 
                            text="Hades II Save Location", 
                            compound=tk.RIGHT) 

save_path_entry = ttk.Entry(root, width=40, state="disabled")
save_path_browse_button = ttk.Button(root, text="Browse")

twitch_connect_label = ttk.Label(root, 
                            image=question_icon, 
                            text="Twitch Connection: Checking...", 
                            compound=tk.RIGHT) 
twitch_profile_label = ttk.Label(root, 
                            image=question_icon) 
twitch_connect_button = ttk.Button(root, text="Connect", state="disabled")
info_label = ttk.Label(root,
                       image=info_icon,
                       text="Argus is active if both checks are passing ✅.\nLeave this window open in the background.",
                       compound=tk.LEFT)