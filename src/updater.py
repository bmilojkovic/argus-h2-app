import os
import requests
import json
import semver
import urllib
import posixpath
import zipfile
import sys
from pathlib import Path

from argus_util import argus_backend, argus_log, argus_version


def get_filename_from_url(url):
    """
    Extracts the filename from a given URL.
    """
    parsed_url = urllib.parse.urlsplit(url)
    path = parsed_url.path
    filename = posixpath.basename(path)
    return filename


executable_directory = Path(sys.executable).parent


def save_file_from_url(download_url):
    response = requests.get(download_url)
    if response.status_code == 200:
        if sys.executable == "updater.exe":
            # make sure this never runs from a .py file
            print("deleting everything")
        filename = os.path.join(
            executable_directory, get_filename_from_url(download_url)
        )
        with open(filename, "wb") as f:
            f.write(response.content)

        return filename
    return None


def update_app():
    update_check_url = argus_backend + "/get_newest_app_version"
    response = requests.get(update_check_url)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if semver.compare(response_json["newest_version"], argus_version) > 0:
            argus_log("Trying to update")
            download_url = argus_backend + response_json["details"]["main_path"]
            filename = save_file_from_url(download_url)

            argus_log(f"Downloaded file {filename}")
            if filename is not None:
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall(executable_directory)
            else:
                argus_log(f"Couldn't download update from url {download_url}. Exiting.")
        else:
            argus_log("Updater activated when there's no update to do. Exiting.")
    else:
        argus_log(
            f"Got bad code from backend: {response.status_code} with response: {response.text}"
        )


if __name__ == "__main__":
    update_app()
