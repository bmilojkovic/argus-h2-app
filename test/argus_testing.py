import configparser
import boto3
import json

import argparse
import sys
import os
import argus_test_generators

test_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(1, test_dir + "../src")

import argus_network

NOBOONS = "NOBOONS"
NOWEAPONS = "NOWEAPONS"
NOFAMILIARS = "NOFAMILIARS"
NOEXTRAS = "NOEXTRAS"
NOELEMENTS = "NOELEMENTS"
NOPINS = "NOPINS"
NOVOWS = "NOVOWS"
NOARCANA = "NOARCANA"

BUCKET_NAME = "argus-h2-backend-argus-tokens"
# BUCKET_NAME = "argus-h2-backend-argus-tokens-test"
UI_MAPPINGS_KEY = "uiMappings"

GENERATOR_CONFIG_FILE = test_dir + "generator_params.ini"


# This uses AWS data so we have a single source of truth.
# If you want to run the test yourself,
# you can find the uiMappings JSON file on the Argus backend repository
# (https://github.com/bmilojkovic/argus-h2-backend)
# and change this function to use that file instead
def generate_test_data():
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=UI_MAPPINGS_KEY)
    ui_mappings_string = response["Body"].read().decode("utf-8")
    ui_mappings = json.loads(ui_mappings_string)

    generator_params = configparser.ConfigParser()
    generator_params.read(GENERATOR_CONFIG_FILE)

    boon_data = argus_test_generators.boon_data_generator(
        ui_mappings, generator_params["boons"]
    )
    weapon_data = argus_test_generators.weapon_data_generator(
        ui_mappings, generator_params["weapons"]
    )
    familiar_data = argus_test_generators.familiar_data_generator(
        ui_mappings, generator_params["familiars"]
    )
    extra_data = argus_test_generators.keepsake_data_generator(
        ui_mappings, generator_params["keepsakes"]
    )
    elemental_data = argus_test_generators.elemental_data_generator(
        ui_mappings, generator_params["elements"]
    )
    pin_data = argus_test_generators.pin_data_generator(
        ui_mappings, generator_params["pins"]
    )
    vow_data = argus_test_generators.vow_data_generator(
        ui_mappings, generator_params["vows"]
    )
    arcana_data = argus_test_generators.arcana_data_generator(
        ui_mappings, generator_params["arcana"]
    )

    return (
        boon_data,
        weapon_data,
        familiar_data,
        extra_data,
        elemental_data,
        pin_data,
        vow_data,
        arcana_data,
    )


def get_test_data(which_test):
    if which_test == "nominal":
        boon_data = "Common;;ApolloManaBoon Rare;;AphroditeSpecialBoon Epic;;PoseidonWeaponBoon Heroic;;PoseidonCastBoon Common;;DaggerBlinkAoETrait Duo;;PoseidonSplashSprintBoon Rare;;DoubleRewardBoon Legendary;;AmplifyConeBoon Infusion;;ElementalDodgeBoon"
        weapon_data = "Rare;;DaggerBlockAspect"
        familiar_data = (
            "8;;LastStandFamiliar 2;;LastStandFamiliar 3;;FamiliarCatResourceBonus"
        )
        extra_data = "Epic;;ForceZeusBoonKeepsake Common;;SpellSummonTrait"
        elemental_data = "Fire:1;;Water:0;;Earth:3;;Air:0;;Aether:0"
        pin_data = "RandomStatusBoon;;AresExCastBoon;;GoodStuffBoon"
        vow_data = "4;;BossDifficultyShrineUpgrade 1;;MinibossCountShrineUpgrade 2;;NextBiomeEnemyShrineUpgrade 2;;BiomeSpeedShrineUpgrade"
        arcana_data = "3;;PanelRerollMetaUpgrade 3;;EffectVulnerabilityMetaUpgrade 2;;ChannelSlowMetaUpgrade 3;;DoorHealMetaUpgrade 3;;LowManaDamageMetaupgrade 1;;CastDamageMetaUpgrade 3;;SorceryRegenMetaUpgrade"
    elif which_test == "minimal":
        boon_data = "Common;;ApolloWeaponBoon"
        weapon_data = NOWEAPONS
        familiar_data = NOFAMILIARS
        extra_data = NOEXTRAS
        elemental_data = NOELEMENTS
        pin_data = NOPINS
        vow_data = NOVOWS
        arcana_data = NOARCANA
    elif which_test == "doubleboon":
        boon_data = "Common;;ApolloManaBoon Rare;;AphroditeSpecialBoon Epic;;PoseidonWeaponBoon Heroic;;PoseidonCastBoon Common;;DaggerBlinkAoETrait Duo;;PoseidonSplashSprintBoon Rare;;DoubleRewardBoon Legendary;;AmplifyConeBoon Infusion;;ElementalDodgeBoon Duo;;PoseidonSplashSprintBoon"
        weapon_data = "Rare;;DaggerBlockAspect"
        familiar_data = (
            "8;;LastStandFamiliar 2;;LastStandFamiliar 3;;FamiliarCatResourceBonus"
        )
        extra_data = "Epic;;ForceZeusBoonKeepsake Common;;SpellSummonTrait"
        elemental_data = "Fire:1;;Water:0;;Earth:3;;Air:0;;Aether:0"
        pin_data = "RandomStatusBoon;;AresExCastBoon;;GoodStuffBoon"
        vow_data = "4;;BossDifficultyShrineUpgrade 1;;MinibossCountShrineUpgrade 2;;NextBiomeEnemyShrineUpgrade 2;;BiomeSpeedShrineUpgrade"
        arcana_data = "3;;PanelRerollMetaUpgrade 3;;EffectVulnerabilityMetaUpgrade 2;;ChannelSlowMetaUpgrade 3;;DoorHealMetaUpgrade 3;;LowManaDamageMetaupgrade 1;;CastDamageMetaUpgrade 3;;SorceryRegenMetaUpgrade"
    elif which_test == "pins":
        boon_data = "Common;;ApolloManaBoon Rare;;AphroditeSpecialBoon Epic;;PoseidonWeaponBoon Heroic;;PoseidonCastBoon Common;;DaggerBlinkAoETrait Duo;;PoseidonSplashSprintBoon Rare;;DoubleRewardBoon Legendary;;AmplifyConeBoon Infusion;;ElementalDodgeBoon"
        weapon_data = "Rare;;DaggerBlockAspect"
        familiar_data = (
            "8;;LastStandFamiliar 2;;LastStandFamiliar 3;;FamiliarCatResourceBonus"
        )
        extra_data = "Epic;;ForceZeusBoonKeepsake Common;;SpellSummonTrait"
        elemental_data = "Fire:1;;Water:0;;Earth:3;;Air:0;;Aether:0"
        pin_data = "LuckyBoon;;ElementalUnifiedBoon;;GoodStuffBoon"
        vow_data = "4;;BossDifficultyShrineUpgrade 1;;MinibossCountShrineUpgrade 2;;NextBiomeEnemyShrineUpgrade 2;;BiomeSpeedShrineUpgrade"
        arcana_data = "3;;PanelRerollMetaUpgrade 3;;EffectVulnerabilityMetaUpgrade 2;;ChannelSlowMetaUpgrade 3;;DoorHealMetaUpgrade 3;;LowManaDamageMetaupgrade 1;;CastDamageMetaUpgrade 3;;SorceryRegenMetaUpgrade"
    else:
        boon_data = NOBOONS
        weapon_data = NOWEAPONS
        familiar_data = NOFAMILIARS
        extra_data = NOEXTRAS
        elemental_data = NOELEMENTS
        pin_data = NOPINS
        vow_data = NOVOWS
        arcana_data = NOARCANA
    return (
        boon_data,
        weapon_data,
        familiar_data,
        extra_data,
        elemental_data,
        pin_data,
        vow_data,
        arcana_data,
    )


def main():
    if args["generate"]:
        (
            boon_data,
            weapon_data,
            familiar_data,
            extra_data,
            elemental_data,
            pin_data,
            vow_data,
            arcana_data,
        ) = generate_test_data()
    else:
        (
            boon_data,
            weapon_data,
            familiar_data,
            extra_data,
            elemental_data,
            pin_data,
            vow_data,
            arcana_data,
        ) = get_test_data(args["prepared"])

        argus_network.send_run_data(
            {
                "boonData": boon_data,
                "weaponData": weapon_data,
                "familiarData": familiar_data,
                "extraData": extra_data,
                "elementalData": elemental_data,
                "pinData": pin_data,
                "vowData": vow_data,
                "arcanaData": arcana_data,
            }
        )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Test the backend and frontend with prepared or generated data."
    )
    arg_parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate a random test based on parameters.",
    )
    arg_parser.add_argument(
        "--prepared",
        choices=["nominal", "minimal", "doubleboon", "pins"],
        help="Run one of the prepared tests.",
    )

    args = vars(arg_parser.parse_args())
    main()
