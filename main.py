import asyncio
from async_tkinter_loop import async_mainloop
from argus_gui import check_twitch_connection, make_gui

import argus_gui_components
from argus_observing import observer_loop



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