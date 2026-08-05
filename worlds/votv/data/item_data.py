from functools import reduce
from math import inf
from typing import TYPE_CHECKING, Callable, NamedTuple
from BaseClasses import ItemClassification as IC

from ..Options import ATVUpgradesAsItems, ArgemiaPlushes, PhysicalModulesAsItems, UpgradesAsItems, WorldItems
from ..Utils import day_item_count, furfur_plush_enabled, is_goal_enabled, resolve
from ..Types import VOTVGoal

if TYPE_CHECKING:
    from .. import VOTVWorld
    Classification = dict[IC, int]
    DynamicClassification = Callable[[VOTVWorld], dict[IC, int]]
    ClassificationResolvable = dict[IC, int] | DynamicClassification

class ExtraItem(NamedTuple):
    classification: "ClassificationResolvable"
    world_item_tier: int | None = WorldItems.option_main

def goal_item(goals: set[VOTVGoal], classification: "ClassificationResolvable") -> "DynamicClassification":
    def resolve_goal_item(world: "VOTVWorld"):
        # The item's objective is active: override all other filters and set all classification to progression
        if world.options.objective.value in goals:
            copy = world.options.as_dict(
                "argemia_plushes",
                # "world_items",
                "buried_items",
                "time_sensitive",
                "scrap_recipes_as_items",
                "funny_setting",
                "upgrades_as_items",
                "physical_modules_as_items",
                "atv_upgrades_as_items"
            )

            world.options.argemia_plushes.value = ArgemiaPlushes.option_all
            # world.options.world_items.value = WorldItems.option_all
            world.options.buried_items.value = 1
            world.options.time_sensitive.value = 1
            world.options.scrap_recipes_as_items.value = 1
            world.options.funny_setting.value = 1
            world.options.upgrades_as_items.value = UpgradesAsItems.option_all
            world.options.physical_modules_as_items.value = PhysicalModulesAsItems.option_all
            world.options.atv_upgrades_as_items.value = ATVUpgradesAsItems.option_all

            result = resolve(plus(*({IC.progression: v} for v in resolve(classification, world).values())), world)

            world.options.argemia_plushes.value = copy["argemia_plushes"]
            # world.options.world_items.value = copy["world_items"]
            world.options.buried_items.value = copy["buried_items"]
            world.options.time_sensitive.value = copy["time_sensitive"]
            world.options.scrap_recipes_as_items.value = copy["scrap_recipes_as_items"]
            world.options.funny_setting.value = copy["funny_setting"]
            world.options.upgrades_as_items.value = copy["upgrades_as_items"]
            world.options.physical_modules_as_items.value = copy["physical_modules_as_items"]
            world.options.atv_upgrades_as_items.value = copy["atv_upgrades_as_items"]

            return result

        if any(is_goal_enabled(world, x) for x in goals):
            return resolve(classification, world)
        
        return {}

    return resolve_goal_item

def argemia_plush(setting: int, classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.argemia_plushes.value >= setting else {}

def buried(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.buried_items.value else {}

def time_sensitive(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.time_sensitive.value else {}

def recipe(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.scrap_recipes_as_items.value else {}

def funny(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.funny_setting.value else {}

def door(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: resolve(classification, world) if world.options.doors_as_items.value else {}

def upgrade(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: {
        k: v for k, v in resolve(classification, world).items()
        if world.options.upgrades_as_items.value == UpgradesAsItems.option_all
        or world.options.upgrades_as_items.value == UpgradesAsItems.option_useful and (k & IC.progression or k & IC.useful)
    }

def module(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: {
        k: v for k, v in resolve(classification, world).items()
        if world.options.physical_modules_as_items.value == PhysicalModulesAsItems.option_all
        or world.options.physical_modules_as_items.value == PhysicalModulesAsItems.option_useful and (k & IC.progression or k & IC.useful)
    }

def atv_upgrade(classification: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: {
        k: v for k, v in resolve(classification, world).items()
        if world.options.atv_upgrades_as_items.value == ATVUpgradesAsItems.option_all
        or world.options.atv_upgrades_as_items.value == ATVUpgradesAsItems.option_useful and (k & IC.progression or k & IC.useful)
    }

def plus(*args: "ClassificationResolvable") -> "DynamicClassification":
    return lambda world: {
        k: sum(resolve(x, world)[k] if k in resolve(x, world) else 0 for x in args)
        for k in reduce(lambda acc, x: {*acc, *resolve(x, world).keys()}, args, set())
    }

def crafted_capsule(amount: int) -> "DynamicClassification":
    return lambda world: {IC.progression: 1, IC.filler: amount - 1} if world.options.enable_crafted_capsule.value else {IC.filler: amount}

goal_items = {
    "Metal Detector":                   ExtraItem(lambda world: {IC.progression: 1} if world.options.buried_items.value else goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})(world)),
    "Kerfur-Omega Complete Manual":     ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Red Kerfur":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Blue Kerfur":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Pink Kerfur":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Omega AI Module":                  ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Ball Joint":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, buried({IC.useful: 8, IC.filler: 4}))),
    "Limb Joint":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 4, IC.filler: 2})),
    "Progressive Camera":               ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 3})),
    "Hacksaw":                          ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, crafted_capsule(1))),
    "Pickaxe":                          ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, crafted_capsule(1))),
    "Hazmat Suit":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, crafted_capsule(1))),
    "Gas Welder":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, crafted_capsule(3))),
    "Radioactive Capsule Blueprint":    ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, crafted_capsule(1))),
    "Radioactive Capsule":              ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, buried({IC.useful: 1}))),

    "Skull":                            ExtraItem(goal_item({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, plus({IC.filler: 5}, buried({IC.filler: 2})))),

    "Red Argemia Plush":                ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Blue Argemia Plush":               ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Green Argemia Plush":              ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Yellow Argemia Plush":             ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Magenta Argemia Plush":            ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Cyan Argemia Plush":               ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Shrimp Pack":                      ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.progression: 17}))),

    "Balloon Pack (WIP)":               ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.progression: 1})),
    "Fire Rune":                        ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Earth Rune":                       ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, buried(time_sensitive({IC.filler: 1})))),
    "Water Rune":                       ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Air Rune":                         ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Ritual Knife":                     ExtraItem(lambda world: {IC.progression: 1} if furfur_plush_enabled(world) else goal_item({VOTVGoal.LAMBERT_PLUSH}, time_sensitive({IC.filler: 1}))(world)),

    "Tile":                             ExtraItem(goal_item({VOTVGoal.GREEN_CABINET}, {IC.filler: 9}))
}

extra_items = {
    "Alpha Base Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Signal Lab Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Server Room Entrance":                             ExtraItem(door({IC.progression: 1})),
    "Garage Entrance":                                  ExtraItem(door({IC.progression: 1})),
    "Admin Room Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Break Room Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Utility Closet Entrance":                          ExtraItem(door({IC.progression: 1})),
    "Alpha Stairs Entrance":                            ExtraItem(door({IC.progression: 1})),
    "Storage Room Entrance":                            ExtraItem(door({IC.progression: 1})),
    "Staff Room Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Bathroom Entrance":                                ExtraItem(door({IC.progression: 1})),
    "Alpha Roof Entrance":                              ExtraItem(door({IC.progression: 1})),
    "Bunker Entrance":                                  ExtraItem(door({IC.progression: 1})),

    "TR1 Room Entrance":                                ExtraItem(door({IC.progression: 1})),
    "TR2 Room Entrance":                                ExtraItem(door({IC.progression: 1})),
    "TR3 Room Entrance":                                ExtraItem(door({IC.progression: 1})),

    "Half Hook":                                        ExtraItem({IC.progression: 2}),
    "Shovel":                                           ExtraItem({IC.progression: 1, IC.useful: 3}),
    "Bunker Keycard":                                   ExtraItem({IC.progression: 1}),
    "Scuba Mask":                                       ExtraItem({IC.progression: 1}),
    "Scuba Mask Tank":                                  ExtraItem({IC.progression: 1}),
    "Metal Scrap Recipe":                               ExtraItem(recipe({IC.progression: 1})),
    "Electronic Scrap Recipe":                          ExtraItem(recipe({IC.progression: 1})),
    "Glass Scrap Recipe":                               ExtraItem(recipe({IC.progression: 1})),
    "Plastic Scrap Recipe":                             ExtraItem(recipe({IC.progression: 1})),
    "Progressive Processing Level":                     ExtraItem(upgrade({IC.progression: 3})),
    "Lifecrystal Signal":                               ExtraItem(lambda world: {IC.progression: 1} if any(is_goal_enabled(world, x) for x in {VOTVGoal.HELL_ROCK, VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}) else {}),
    "Hiking Boots":                                     ExtraItem({IC.progression: 1}),
    "Lighter":                                          ExtraItem({IC.progression: 1}),
    "Cig Pack":                                         ExtraItem({IC.progression: 1}),
    "Sponge":                                           ExtraItem(lambda world: {IC.progression: 1} if world.options.maintenance_tasks.value else {}),
    "Fuse":                                             ExtraItem(lambda world: {IC.progression: 10} if world.options.fuse_replacement_locations.value else {}),
    "Crowbar":                                          ExtraItem(lambda world: {(IC.progression if world.options.chicken_sandwiches.value else IC.useful): 1}),
    "Day":                                              ExtraItem(lambda world: {IC.progression: day_item_count(world)} if world.options.day_as_items.value else {}),

    "Furfur Altar Leg 1":                               ExtraItem(lambda world: time_sensitive({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1})(world)),
    "Furfur Altar Leg 2":                               ExtraItem(lambda world: buried({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1})(world)),
    "Furfur Altar Top":                                 ExtraItem(lambda world: buried(time_sensitive({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1}))(world)),

    # "Lead Pipe":                                        ExtraItem({IC.useful: 1}),
    "Axe":                                              ExtraItem({IC.useful: 1}),
    "Gas Can":                                          ExtraItem({IC.useful: 1}),
    "Bike Helmet":                                      ExtraItem({IC.useful: 1}),
    "Digital Map":                                      ExtraItem({IC.useful: 1}),
    "Progressive Processing Speed":                     ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Download Speed":                       ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Detector Strength":                    ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Cursor Drift":                         ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Cursor Speed":                         ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Ping Cooldown":                        ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Ping Speed":                           ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Physical Module (Storm Filter)":                   ExtraItem(module({IC.useful: 1})),
    "Physical Module (Automatic Polarity Adjustment)":  ExtraItem(module({IC.useful: 1})),
    "Physical Module (Automatic Signal Processing)":    ExtraItem(module({IC.useful: 1})),
    "Physical Module (Global Alert)":                   ExtraItem(module({IC.useful: 1})),
    "Physical Module (Coordinate Triangle Visualise)":  ExtraItem(module({IC.useful: 1})),
    "Physical Module (Radar Colors)":                   ExtraItem(module({IC.useful: 1})),
    "ATV Upgrade (Big Lights)":                         ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Bumper)":                             ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Belt)":                               ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Overcharged Engine)":                 ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Alternator)":                         ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Container)":                          ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Solar Panel)":                        ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Map)":                                ExtraItem(atv_upgrade({IC.useful: 1})),
    "Rubber Scrap Recipe":                              ExtraItem(recipe({IC.useful: 1})),
    "Paper Scrap Recipe":                               ExtraItem(recipe({IC.useful: 1})),
    "Wood Scrap Recipe":                                ExtraItem(recipe({IC.useful: 1})),
    "Progressive Sleeping Bag":                         ExtraItem({IC.useful: 3}),
    "Toolbox":                                          ExtraItem({IC.useful: 1, IC.filler: 3}),
    "Car Battery Charger":                              ExtraItem({IC.useful: 1}),
    "First Aid Medkit":                                 ExtraItem({IC.useful: 1}),
    "Jar of Honey":                                     ExtraItem({IC.useful: 1}),
    "ATV wheel":                                        ExtraItem({IC.useful: 1}),

    "Chicken Sandwich":                                 ExtraItem(plus({IC.filler: 19}, buried({IC.filler: 1}), time_sensitive({IC.filler: 1}))),
    "Rubble Recipe":                                    ExtraItem(recipe({IC.filler: 1})),
    "Air Tablet":                                       ExtraItem(buried({IC.filler: 1})),
    "Fire Tablet":                                      ExtraItem(buried({IC.filler: 1})),
    "Earth Tablet":                                     ExtraItem(buried({IC.filler: 1})),
    "Water Tablet":                                     ExtraItem(buried({IC.filler: 1})),
    "Progressive Radar History":                        ExtraItem(upgrade({IC.filler: 3})),
    "Progressive Radar Speed":                          ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Detector Frequency":                   ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Detector Quality":                     ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Coordinate Speed":                     ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Breaker Time":                         ExtraItem(upgrade({IC.filler: 16})),
    "Physical Module (Radar Alarm)":                    ExtraItem(module({IC.filler: 1})),
    "Physical Module (Radar Radius)":                   ExtraItem(module({IC.filler: 1})),
    "Physical Module (Radar Path Tracking)":            ExtraItem(module({IC.filler: 1})),
    "Physical Module (Radar Radial Search)":            ExtraItem(module({IC.filler: 1})),
    "Physical Module (Autosave Signal to Database)":    ExtraItem(module({IC.filler: 1})),
    "Physical Module (Log Tapes Compression)":          ExtraItem(module({IC.filler: 1})),
    "Physical Module (Lightning Prediction)":           ExtraItem(module({IC.filler: 1})),
    "Physical Module (Spectrogram)":                    ExtraItem(module({IC.filler: 1})),
    "Physical Module (Remote Keyboard)":                ExtraItem(module({IC.filler: 1})),
    "ATV Upgrade (Radio)":                              ExtraItem(atv_upgrade({IC.filler: 1})),
    "ATV Upgrade (Floaties)":                           ExtraItem(atv_upgrade({IC.filler: 1})),
    "ATV Upgrade (Air Control)":                        ExtraItem(atv_upgrade({IC.filler: 1})),
    "Kerfur-Omega Documents Binder":                    ExtraItem({IC.filler: 1}),
    "Geiger Counter":                                   ExtraItem({IC.filler: 1}),
    "EMF Detector":                                     ExtraItem(buried({IC.filler: 1})),
    # "Lantern":                                          ExtraItem({IC.filler: 1}),
    "Watering Can":                                     ExtraItem({IC.filler: 3}),
    "Deer Skull":                                       ExtraItem({IC.filler: 1}),
    "Antibreather Plush":                               ExtraItem(time_sensitive({IC.filler: 1})),
    "Erie Plush":                                       ExtraItem(buried(time_sensitive({IC.filler: 1}))),
    "Monique Plush":                                    ExtraItem({IC.filler: 1}),
    "Furfur Plush":                                     ExtraItem(lambda world: {IC.filler: 1} if furfur_plush_enabled(world) else {}),
    "Cacti":                                            ExtraItem(buried({IC.filler: 1})),
    "Librarian Candle":                                 ExtraItem(buried({IC.filler: 1})),
    "Car Keys":                                         ExtraItem({IC.filler: 1}),
    "Cooking Book":                                     ExtraItem({IC.filler: 1}),
    "Nuclear Pink Argemia Plush":                       ExtraItem(argemia_plush(ArgemiaPlushes.option_all, {IC.filler: 1})),
    "Nuclear Yellow Argemia Plush":                     ExtraItem(argemia_plush(ArgemiaPlushes.option_all, buried({IC.filler: 1}))),
    "Nuclear Orange Argemia Plush":                     ExtraItem(argemia_plush(ArgemiaPlushes.option_all, {IC.filler: 1})),
    "Seed Pack (The Thingy)":                           ExtraItem({IC.filler: 1}),
    "\"Svenskfisk\"":                                   ExtraItem({IC.filler: 1}),
    "Tinfoil Hat":                                      ExtraItem({IC.filler: 1}),
    "Old Rifle":                                        ExtraItem({IC.filler: 1}),
    "Ammo Box":                                         ExtraItem({IC.filler: 1}),
    "Wall Clock":                                       ExtraItem({IC.filler: 1}),
    "Unknown Fruit":                                    ExtraItem({IC.filler: 1}),
    "Bowtie":                                           ExtraItem({IC.filler: 2}),
    "Glasses":                                          ExtraItem({IC.filler: 2}),
    "Badge":                                            ExtraItem({IC.filler: 2}),
    "Jacket":                                           ExtraItem({IC.filler: 2}),
    "Compost Bucket":                                   ExtraItem({IC.filler: 2}),
    "Green Fire Rock":                                  ExtraItem(time_sensitive({IC.filler: 1})),
    "Broom":                                            ExtraItem({IC.filler: 2}),
    "Pipebomb":                                         ExtraItem({IC.filler: 1}),
    "Welding Mask":                                     ExtraItem({IC.filler: 2}),
    "Boar Trophy Head":                                 ExtraItem({IC.filler: 1}),
    "Deer Trophy Head":                                 ExtraItem({IC.filler: 1}),
    "Goat Trophy Head":                                 ExtraItem({IC.filler: 1}),
    "Bonus Points":                                     ExtraItem({IC.filler: 1}),

    # Previously shuffled, but I think it's better to just have the player keep them when found
    # "Maxwell":                                          ExtraItem(funny({IC.filler: 1})),
    # "Argemwell":                                        ExtraItem(funny({IC.filler: 1})),
    # "Gnarpwell":                                        ExtraItem(funny({IC.filler: 1})),
    # "Eriewell":                                         ExtraItem(funny({IC.filler: 1})),
    "Thiccfus Plush":                                   ExtraItem(funny({IC.filler: 1})),
    "Perkele Llama":                                    ExtraItem(funny({IC.filler: 1})),
    "Maid outfit":                                      ExtraItem(funny(buried({IC.filler: 1}))),

    "Ragdoll Trap":                                     ExtraItem({IC.trap: 1}),
    "Breaker Trap":                                     ExtraItem({IC.trap: 1}),
    # Disabled as it's not that big of a trap and can mess with access to regions
    # "Debug TP Trap":                                    ExtraItem({IC.trap: 1}),
    "Drunk Trap":                                       ExtraItem({IC.trap: 1}),
    "Points Fine Trap":                                 ExtraItem({IC.trap: 1}),
    "Flat Tire Trap":                                   ExtraItem({IC.trap: 1}),
    "Dead Flashlight Trap":                             ExtraItem({IC.trap: 1})
}
