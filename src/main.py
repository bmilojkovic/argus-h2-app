import requests
import json
import semver
import asyncio
from async_tkinter_loop import async_mainloop
from argus_gui import check_twitch_connection, make_main_gui, make_update_gui

import argus_gui_components
from argus_observing import observer_loop

from argus_util import argus_backend, argus_version, argus_log


def update_check():
    update_check_url = argus_backend + "/get_newest_app_version"
    response = requests.get(update_check_url)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if semver.compare(response_json["newest_version"], argus_version) > 0:
            make_update_gui(response_json["details"])
            return True
        else:
            return False

    else:
        argus_log(f"Update check got code {response.status_code}")

    return True


def main():
    check_event_loop = asyncio.new_event_loop()
    if not update_check():
        make_main_gui()

        # set up the twitch check task that we want to do in the background on startup
        check_event_loop.create_task(check_twitch_connection())
        check_event_loop.create_task(observer_loop())

    # start the Tkinter event loop
    async_mainloop(argus_gui_components.root, check_event_loop)


if __name__ == "__main__":
    main()
