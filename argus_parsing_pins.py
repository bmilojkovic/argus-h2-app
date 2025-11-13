from argus_util import DATA_SEPARATOR


def build_pin_data(all_pins):
    pin_data = ""

    for pin in all_pins:
        if "Name" in pin:
            pin_data += pin["Name"] + DATA_SEPARATOR

    # cut off the last data separator
    if len(pin_data) > 0:
        pin_data = pin_data[: -len(DATA_SEPARATOR)]

    return pin_data
