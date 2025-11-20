from argus_parsing_elements import build_elemental_data
from argus_parsing_familiars import build_familiar_data
from argus_parsing_identifiers import (
    is_arcana,
    is_boon_with_rarity,
    is_extra_boon,
    is_familiar,
    is_weapon,
)
from argus_parsing_pins import build_pin_data
from argus_parsing_vows import build_vow_data
from argus_util import DATA_SEPARATOR, argus_log


def read_rarity(trait):
    if "IsElementalTrait" in trait and trait["IsElementalTrait"]:
        return "Infusion"
    if "Rarity" not in trait:
        return "Common"
    return trait["Rarity"]


def read_rarity_and_name(trait):
    rarity = read_rarity(trait)
    return rarity + DATA_SEPARATOR + trait["Name"]


arcana_rarity_mapping = {
    "Common": "1",
    "Rare": "2",
    "Epic": "3",
    "Heroic": "4",
}


def read_arcana(arcana_trait):
    arcana_rarity = "1"

    if "Rarity" in arcana_trait:
        arcana_rarity = arcana_rarity_mapping[arcana_trait["Rarity"]]

    return arcana_rarity + DATA_SEPARATOR + arcana_trait["Name"]


def clean_parsed_data(parsed_data):
    if parsed_data["boonData"] == "":
        parsed_data["boonData"] = "NOBOONS"
    if parsed_data["extraData"] == "":
        parsed_data["extraData"] = "NOEXTRAS"
    if parsed_data["weaponData"] == "":
        parsed_data["weaponData"] = "NOWEAPONS"
    if parsed_data["familiarData"] == "":
        parsed_data["familiarData"] = "NOFAMILIARS"
    if parsed_data["elementalData"] == "":
        parsed_data["elementalData"] = "NOELEMENTS"
    if parsed_data["vowData"] == "":
        parsed_data["vowData"] = "NOVOWS"
    if parsed_data["arcanaData"] == "":
        parsed_data["arcanaData"] = "NOARCANA"
    if parsed_data["pinData"] == "":
        parsed_data["pinData"] = "NOPINS"

    for key in parsed_data:
        parsed_data[key] = parsed_data[key].strip()

    return parsed_data


def parse_data(save_data):
    parsed_data = {
        "boonData": "",
        "extraData": "",
        "weaponData": "",
        "familiarData": "",
        "elementalData": "",
        "vowData": "",
        "arcanaData": "",
        "pinData": "",
    }

    if (
        "CurrentRun" not in save_data
        or "Hero" not in save_data["CurrentRun"]
        or "Traits" not in save_data["CurrentRun"]["Hero"]
    ):
        argus_log("Malformed save_data. Couldn't find hero traits.")
        return "INVALID"
    hero_traits = save_data["CurrentRun"]["Hero"]["Traits"]
    for trait in hero_traits:
        if is_boon_with_rarity(trait):
            parsed_data["boonData"] += read_rarity_and_name(trait) + " "
        if is_extra_boon(trait):
            parsed_data["extraData"] += read_rarity_and_name(trait) + " "
        if is_weapon(trait):
            parsed_data["weaponData"] = read_rarity_and_name(trait)
        if is_familiar(trait):
            parsed_data["familiarData"] = build_familiar_data(trait, hero_traits)
        if is_arcana(trait):
            parsed_data["arcanaData"] += read_arcana(trait) + " "

    if parsed_data["weaponData"] == "":
        argus_log("Couldn't find weapon data.")
        return "INVALID"

    if parsed_data["familiarData"] == "INVALID":
        argus_log("Incomplete familiar data.")
        return "INVALID"

    if "Elements" in save_data["CurrentRun"]["Hero"]:
        hero_elements = save_data["CurrentRun"]["Hero"]["Elements"]
        parsed_data["elementalData"] = build_elemental_data(hero_elements)

    if "StoreItemPins" in save_data["GameState"]:
        all_pins = save_data["GameState"]["StoreItemPins"]
        parsed_data["pinData"] = build_pin_data(all_pins)

    if "ShrineUpgrades" in save_data["GameState"]:
        all_vows = save_data["GameState"]["ShrineUpgrades"]
        parsed_data["vowData"] = build_vow_data(all_vows)

    return clean_parsed_data(parsed_data)
