from argus_util import DATA_SEPARATOR


familiar_level_trait_map = {
    "HealthFamiliar": {
        "HealthFamiliar",
        "FamiliarFrogResourceBonus",
        "FamiliarFrogDamage",
    },
    "CritFamiliar": {
        "CritFamiliar",
        "FamiliarRavenResourceBonus",
        "FamiliarRavenAttackDuration",
    },
    "LastStandFamiliar": {
        "LastStandFamiliar",
        "FamiliarCatResourceBonus",
        "FamiliarCatAttacks",
    },
    "DigFamiliar": {
        "DigFamiliar",
        "FamiliarHoundResourceBonus",
        "FamiliarHoundBarkDuration",
    },
    "DodgeFamiliar": {
        "DodgeFamiliar",
        "FamiliarPolecatResourceBonus",
        "FamiliarPolecatDamage",
    },
}


def count_familiar_level(familiar_name, hero_traits):
    if familiar_name not in familiar_level_trait_map:
        return 1

    possible_familiar_traits = familiar_level_trait_map[familiar_name]

    count = 1

    for hero_trait in hero_traits:
        if (
            "Name" in hero_trait
            and "StackNum" in hero_trait
            and hero_trait["Name"] in possible_familiar_traits
        ):
            count = count + int(hero_trait["StackNum"]) - 1

    return count


familiar_trait_map = {
    "HealthFamiliar": {"HealthFamiliar", "FamiliarFrogResourceBonus"},
    "CritFamiliar": {"CritFamiliar", "FamiliarRavenResourceBonus"},
    "LastStandFamiliar": {"LastStandFamiliar", "FamiliarCatResourceBonus"},
    "DigFamiliar": {"DigFamiliar", "FamiliarHoundResourceBonus"},
    "DodgeFamiliar": {"DodgeFamiliar", "FamiliarPolecatResourceBonus"},
}


def build_familiar_data(familiar_trait, hero_traits):
    if "Name" not in familiar_trait:
        return "NOFAMILIARS"

    familiar_name = familiar_trait["Name"]
    familiar_level = count_familiar_level(familiar_name, hero_traits)

    familiar_string = str(familiar_level) + DATA_SEPARATOR + familiar_name

    familiar_traits = familiar_trait_map[familiar_name]
    trait_counter = 1

    for added_trait in familiar_traits:
        for hero_trait in hero_traits:
            if (
                "Name" in hero_trait
                and "StackNum" in hero_trait
                and hero_trait["Name"] == added_trait
            ):
                familiar_string = (
                    familiar_string
                    + " "
                    + str(hero_trait["StackNum"])
                    + DATA_SEPARATOR
                    + hero_trait["Name"]
                )
                trait_counter += 1

    if trait_counter != 3:
        return "INVALID"

    return familiar_string
