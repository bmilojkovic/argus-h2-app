import requests
import json
import semver

from argus_util import argus_backend, argus_version


def save_file_from_url(download_url):
    reponse = requests.get(download_url)
    if reponse.status_code == 200:
        print()


def update_app():
    update_check_url = argus_backend + "/get_newest_app_version"
    response = requests.get(update_check_url)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if semver.compare(response_json["newest_version"], argus_version) > 0:
            download_url = argus_backend + response_json["details"]["main_path"]
            save_file_from_url(download_url)
        else:
            print("updating when there's no update to do")
    else:
        print("error log")


if __name__ == "__main__":
    update_app()
