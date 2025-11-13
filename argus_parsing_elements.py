from argus_util import DATA_SEPARATOR


def build_elemental_data(hero_elements):
    elements = {"Fire", "Air", "Earth", "Water", "Aether"}

    elements_string = ""

    for element in elements:
        elements_string = (
            elements_string
            + element
            + ":"
            + str(hero_elements[element])
            + DATA_SEPARATOR
        )

    # cut off the last data separator
    if len(elements_string) > 0:
        elements_string = elements_string[: -len(DATA_SEPARATOR)]

    return elements_string
