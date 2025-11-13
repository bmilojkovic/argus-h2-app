from argus_parsing_identifiers import is_vow
from argus_util import DATA_SEPARATOR


def build_vow_data(all_vows):
    vow_string = ""

    for vow_name in all_vows.keys():
        if is_vow(vow_name):
            vow_level = all_vows[vow_name]
            if vow_level != 0:
                vow_string = (
                    vow_string + str(vow_level) + DATA_SEPARATOR + str(vow_name) + " "
                )

    return vow_string
