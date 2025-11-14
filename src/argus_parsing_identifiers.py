from argus_parsing_data import argus_parsing_data


def is_in_list(trait, trait_list):
    return "Name" in trait and trait["Name"] in trait_list


def is_chaos_blessing(trait):
    return (
        "Name" in trait
        and trait["Name"].startswith("Chaos")
        and trait["Name"].endswith("Blessing")
    )


def is_chaos_curse(trait):
    return (
        "Name" in trait
        and trait["Name"].startswith("Chaos")
        and trait["Name"].endswith("Curse")
    )


def is_hammer(trait):
    return "IsHammerTrait" in trait and trait["IsHammerTrait"]


def is_keepsake(trait):
    return "Slot" in trait and trait["Slot"] == "Keepsake"


def is_hex(trait):
    return "Slot" in trait and trait["Slot"] == "Spell"


def is_weapon(trait):
    return "Slot" in trait and trait["Slot"] == "Aspect"


def is_familiar(trait):
    return "Slot" in trait and trait["Slot"] == "Familiar"


def is_arcana(trait):
    return is_in_list(trait, argus_parsing_data["arcana"])


def is_vow(vow_name):
    return vow_name in argus_parsing_data["vows"]


def is_boon_with_rarity(trait):
    return (
        is_in_list(trait, argus_parsing_data["gods"])
        or is_chaos_blessing(trait)
        or is_in_list(trait, argus_parsing_data["hades_main"])
        or is_in_list(trait, argus_parsing_data["icarus_main"])
        or is_in_list(trait, argus_parsing_data["medea_main"])
        or is_in_list(trait, argus_parsing_data["circe_main"])
        or is_in_list(trait, argus_parsing_data["athena_main"])
        or is_in_list(trait, argus_parsing_data["arachne"])
        or is_hammer(trait)
    )


def is_extra_boon(trait):
    return (
        is_keepsake(trait)
        or is_hex(trait)
        or is_chaos_curse(trait)
        or is_in_list(trait, argus_parsing_data["hades_extra"])
        or is_in_list(trait, argus_parsing_data["icarus_extra"])
        or is_in_list(trait, argus_parsing_data["medea_extra"])
        or is_in_list(trait, argus_parsing_data["circe_extra"])
        or is_in_list(trait, argus_parsing_data["athena_extra"])
    )
