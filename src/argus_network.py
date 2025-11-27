import asyncio
import requests
from argus_util import argus_log, argus_backend, get_user_data_dir
import urllib
import webbrowser
import secrets
import configparser
import os

extension_id = "sl19e3aebmadlewzt7mxfv3j3llwwv"
config_file_path = os.path.join(get_user_data_dir(), "argus_token.ini")


async def do_argus_auth():
    config = configparser.ConfigParser()
    base_url = "https://id.twitch.tv/oauth2/authorize"
    stateBytes = secrets.token_hex(16)
    claimsString = '{"userinfo": {"picture":null}}'
    params = {
        "response_type": "code",
        "client_id": extension_id,
        "state": stateBytes,
        "redirect_uri": argus_backend + "/oauth_token",
        "scope": urllib.parse.quote_plus("openid"),
        "claims": urllib.parse.quote_plus(claimsString),
    }

    target_url = base_url + "?"

    for key, value in params.items():
        target_url += key + "=" + value + "&"

    webbrowser.open(target_url)
    retries = 60
    while retries > 0:
        response = requests.post(
            argus_backend + "/get_argus_token",
            json={"argusProtocolVersion": "2", "state": stateBytes},
            timeout=60,
        )

        argus_log("asked for argus token and got: " + response.text)
        if response.status_code == 200 and response.text != "FAIL":
            response_data = response.text.split("\n")
            if len(response_data) != 2:
                argus_log("Got strange response data: " + response.text)
                return None, None
            new_argus_token = response_data[0]
            new_profile_pic = response_data[1]
            config["DEFAULT"] = {
                "argus_token": new_argus_token,
                "profile_pic": new_profile_pic,
            }
            with open(config_file_path, "w") as config_file:
                config.write(config_file)
            return new_argus_token, new_profile_pic
        else:
            retries = retries - 1
        await asyncio.sleep(1)
    return None, None


def check_argus_token_ok(argus_token):
    response = requests.get(
        argus_backend + "/check_argus_token",
        params={"argusProtocolVersion": "2", "argus_token": argus_token},
    )
    argus_log("checking token " + argus_token + " and got response " + response.text)
    return response.status_code == 200 and response.text == "token_ok"


def get_argus_token():
    config = configparser.ConfigParser()
    config.read(config_file_path)

    if "DEFAULT" in config and "argus_token" in config["DEFAULT"]:
        argus_token = config["DEFAULT"]["argus_token"]
        profile_pic = config["DEFAULT"]["profile_pic"]
        if check_argus_token_ok(argus_token):
            return argus_token, profile_pic

    return "FAIL", None


def send_run_data(run_data):
    argus_token, _ = get_argus_token()
    if argus_token == "FAIL":
        argus_log("Failed to read argus token from config file.")
    else:
        argus_log("Sending run data: " + str(run_data))
        response = requests.post(
            argus_backend + "/run_info",
            json={
                "argusProtocolVersion": "2",
                "argusToken": argus_token,
                "runData": run_data,
            },
        )
        argus_log("Run info response: " + str(response))
