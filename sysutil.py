
from argus_util import argus_log
import winreg

def get_steam_path():
    """
    Reads the Steam installation path from the Windows registry.
    """
    # List of possible registry keys to check
    possible_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Valve\Steam"),
    ]

    for root_key, sub_key_path in possible_keys:
        try:
            # Open the key with read access
            with winreg.OpenKey(root_key, sub_key_path, 0, winreg.KEY_READ) as key:
                # Read the 'InstallPath' value
                install_path, reg_type = winreg.QueryValueEx(key, "InstallPath")
                argus_log(f"Steam installation path found: {install_path}")
                return install_path
        except FileNotFoundError:
            # Key not found, try the next one
            continue
        except Exception as e:
            argus_log(f"An error occurred while reading registry key '{sub_key_path}': {e}")
            continue
    
    argus_log("Steam installation path not found in the registry.")
    return None