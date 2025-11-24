import random

DATA_SEPARATOR = ";;"

def percentile_boolean(percent):
    return random.randint(0, 99) <= percent

def boon_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""
    
    boon_rarities = ["Common", "Rare", "Epic", "Heroic"]
    boon_data = ""

    boon_count = random.randint(int(generator_params["min_boons"]), int(generator_params["max_boons"]))
    for i in range(boon_count):
        rarity = random.choice(boon_rarities)
        boon = random.choice(list(ui_mappings["boons"].keys()))

        boon_data += rarity + DATA_SEPARATOR + boon + " "

    return boon_data

def weapon_data_generator(ui_mappings, generator_params):
    weapon_rarities = ["Common", "Rare", "Epic", "Legendary", "Perfect"]

    rarity = random.choice(weapon_rarities)
    weapon = random.choice(list(ui_mappings["weapons"].keys()))

    return rarity + DATA_SEPARATOR + weapon

def familiar_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    familiar_level = str(random.randint(1, 10))
    familiar_name = random.choice(list(ui_mappings["familiars"].keys()))

    first_trait = ui_mappings["familiars"][familiar_name]["effects"][0]["codeName"]
    first_trait_level = str(random.randint(1, 4))

    second_trait = ui_mappings["familiars"][familiar_name]["effects"][1]["codeName"]
    second_trait_level = str(random.randint(1, 4))

    return familiar_level + DATA_SEPARATOR + familiar_name + " " + first_trait_level + DATA_SEPARATOR + first_trait + " " + second_trait_level + DATA_SEPARATOR + second_trait

def keepsake_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    keepsake_rarities = ["Common", "Rare", "Epic", "Heroic"]
    keepsake_rarity = random.choice(keepsake_rarities)
    keepsake_name = random.choice(list(ui_mappings["keepsakes"].keys()))

    keepsake_string = keepsake_rarity + DATA_SEPARATOR + keepsake_name

    return keepsake_string

def elemental_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    element_list = ["Fire", "Air", "Earth", "Water", "Aether"]
    element_string = ""

    for element in element_list:
        element_string += element + ":" + str(random.randint(0, int(generator_params["max_value"]))) + DATA_SEPARATOR

    element_string = element_string[:-len(DATA_SEPARATOR)]

    return element_string

def pin_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    pin_count = random.randint(int(generator_params["min_pins"]), int(generator_params["max_pins"]))
    pin_string = ""

    for i in range(pin_count):
        boon = random.choice(list(ui_mappings["boons"].keys()))
        pin_string += boon + DATA_SEPARATOR

    pin_string = pin_string[:-len(DATA_SEPARATOR)]

    return pin_string

def vow_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    vow_string = ""

    for vow_name in ui_mappings["vows"].keys():
        if random.randint(1, 2) == 1: # include this vow
            max_level = len(ui_mappings["vows"][vow_name]["fears"])-1
            vow_level = random.randint(1, max_level)
            vow_string = vow_string + str(vow_level) + DATA_SEPARATOR + vow_name + " "

    return vow_string

def arcana_data_generator(ui_mappings, generator_params):
    include = percentile_boolean(int(generator_params["include"]))
    if not include:
        return ""

    arcana_string = ""

    for arcana_name in ui_mappings["arcana"].keys():
        if random.randint(1, 100) <= int(generator_params["include_card"]): # include this card
            max_level = 4
            arcana_level = random.randint(1, max_level)
            arcana_string = arcana_string + str(arcana_level) + DATA_SEPARATOR + arcana_name + " "

    return arcana_string