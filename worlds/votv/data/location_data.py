from typing import TYPE_CHECKING, Callable, NamedTuple

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAllCounts, HasAny, HasFromList, Rule

from ..Utils import is_goal_enabled, furfur_plush_enabled
from ..Options import ArgemiaPlushes, DayAsItems, ScrapRecipesAsItems, UpgradesAsItems, WorldItems
from ..Types import VOTVGoal
from ..Constants import (
    max_days,
    max_signal_locations,
    max_daily_tasks_locations,
    max_fuse_replacement_locations,
    max_server_repair_locations,
    max_transformer_repair_locations,
    max_trash_cleaning_locations
)

if TYPE_CHECKING:
    from .. import VOTVWorld
    EnabledFunc = Callable[[VOTVWorld], bool]

class LocationInfo(NamedTuple):
    hint: str
    group: str
    rule: Rule | None = None
    enabled: "EnabledFunc" = lambda _: True
    world_item_tier: int | None = WorldItems.option_main

def goal(goals: set[VOTVGoal], final: bool = False, also: "EnabledFunc" = lambda _: True) -> "EnabledFunc" :
    return lambda world: world.options.objective.value in goals or not final and any(is_goal_enabled(world, x) for x in goals) and also(world)

def argemia_plush(setting: int) -> "EnabledFunc":
    return lambda world: world.options.argemia_plushes.value >= setting

def buried(world: "VOTVWorld"):
    return bool(world.options.buried_items.value)

def time_sensitive(world: "VOTVWorld"):
    return bool(world.options.time_sensitive.value)

def funny(world: "VOTVWorld"):
    return bool(world.options.funny_setting.value)

def chicken_sandwich(world: "VOTVWorld"):
    return bool(world.options.chicken_sandwiches.value)

def maintenance(world: "VOTVWorld"):
    return bool(world.options.maintenance_tasks.value)

def cooking(world: "VOTVWorld"):
    return bool(world.options.cooking_tasks.value)

def candles(world: "VOTVWorld"):
    return bool(world.options.rock_candles.value)

def fuse(world: "VOTVWorld"):
    return world.options.fuse_replacement_locations.value > 0

locations = {
    "Spectogram Module":                LocationInfo("In a drawer in the basement", "Alpha Base"),
    "Medkit":                           LocationInfo("In the Administration Office", "Alpha Base"),
    "Car Keys":                         LocationInfo("In the Administration Office", "Alpha Base"),
    "Cooking Book":                     LocationInfo("In the living quarters", "Alpha Base"),
    # Disabled because it requires a specific event that might be skipped
    # "Lead Pipe":                        LocationInfo("In the first vent above when entering the Signal Room", rule=Has("Half Hook")),
    "Miniature Gas Can":                LocationInfo("On top of the garage in a corner", "Alpha Base"),
    "Alpha Toolbox":                    LocationInfo("", "Alpha Base"),
    "ATV Wheel":                        LocationInfo("", "Alpha Base"),
    "Ammo Box":                         LocationInfo("Behind the crates in the garage", "Alpha Base"),
    "Alpha Broom":                      LocationInfo("In the utility closet", "Alpha Base"),
    "Pipebomb":                         LocationInfo("In the corner drawer in the signal room", "Alpha Base"),
    "Sponge":                           LocationInfo("In the signal room", "Alpha Base", enabled=maintenance),
    **{f"Alpha Fuse {i+1}":             LocationInfo("In the upstairs storage room", "Alpha Base", enabled=fuse) for i in range(3)},

    **{f"TR{i+1} Watering Can":         LocationInfo("", f"TR{i+1}") for i in range(3)},
    **{f"TR{i+1} Fuse":                 LocationInfo("", f"TR{i+1}", enabled=fuse) for i in range(3)},
    "TR1 Cigarettes":                   LocationInfo("", "TR1"),
    "TR1 Tinfoil Hat":                  LocationInfo("", "TR1"),
    "TR1 Toolbox":                      LocationInfo("", "TR1"),
    "TR1 Lighter":                      LocationInfo("", "TR1"),
    "TR1 Broom":                        LocationInfo("", "TR1"),
    "TR2 Car Battery Charger":          LocationInfo("", "TR2"),
    "TR2 Shovel":                       LocationInfo("In the rafters", "TR2"),
    "TR3 Hiking Boots":                 LocationInfo("", "TR3"),

    "Hole Toolbox":                     LocationInfo("", "The Hole"),
    "EMF Detector":                     LocationInfo("At the Hole, near a fallen construction light", "The Hole", enabled=buried, rule=HasAll("Shovel", "Metal Detector")),
    "Lantern":                          LocationInfo("At the Hole", "The Hole"),
    "Hole Welding Mask":                LocationInfo("", "The Hole"),

    "Green Hatch Toolbox":              LocationInfo("", "Green Hatch"),
    "Geiger Counter":                   LocationInfo("At the Green Hatch", "Green Hatch"),
    "Green Hatch Welding Mask":         LocationInfo("", "Green Hatch"),

    "Abandoned Shack Shovel":           LocationInfo("", "Abandoned Shack"),
    "Axe":                              LocationInfo("In the Abandoned Shack", "Abandoned Shack"),
    "Deer Skull":                       LocationInfo("In the Abandoned Shack", "Abandoned Shack"),
    "Boar Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack"),
    "Deer Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack"),
    "Goat Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack"),
    "Seed Pack (The Thingy)":           LocationInfo("In the Abandoned Shack", "Abandoned Shack"),

    "Green Fire Rock":                  LocationInfo("Extinguish the green fire in the Village (Day 8+, from 12:00 AM to 1:00 AM)", "Village", enabled=time_sensitive),
    "Compost Bucket 1":                 LocationInfo("In the Village's farm plot", "Village"),
    "Compost Bucket 2":                 LocationInfo("In the Village's farm plot", "Village"),

    "Stonehenge Shovel":                LocationInfo("", "Stonehenge"),
    "Security Booth Shovel":            LocationInfo("", "Misc"),
    "Bike Helmet":                      LocationInfo("On top of the rocks to the right of the security booth", "Misc"),
    "Old Rifle":                        LocationInfo("In Lima's server room", "Misc"),
    "Fisherman's Treasure":             LocationInfo("At 176.06/-460.41", "Misc", enabled=buried, rule=HasAll("Shovel", "Metal Detector")),
    "Well Hook 1":                      LocationInfo("", "Misc", rule=Has("Half Hook")),
    "Well Hook 2":                      LocationInfo("", "Misc", rule=Has("Half Hook")),
    "Jar of Honey":                     LocationInfo("Atop the second utility pole from TR3", "Misc", rule=Has("Half Hook")),
    "Argemia Mug":                      LocationInfo("Atop the utility pole closest to the windmills", "Misc", rule=Has("Half Hook")),
    "Limestone Slab":                   LocationInfo("At 567.0/237.0 near the treehouse", "Misc", enabled=buried, rule=HasAll("Shovel", "Metal Detector")),
    "Antibreather Plush":               LocationInfo("Be in the Cave at 3:33 AM, then look in the larger nest", "Cave", enabled=time_sensitive),
    "Erie Plush":                       LocationInfo("Bury a meat garbage bag at Sierra and wait for 1:00 AM", "Misc", enabled=lambda world: buried(world) and time_sensitive(world), rule=Has("Shovel")),
    "Librarian Candle":                 LocationInfo("In the log under the lake surface", "Lake", enabled=buried, rule=Has("Shovel")),
    "Dream Plush":                      LocationInfo("Buried near the bottom side of the Lake", "Lake", enabled=buried, rule=HasAll("Shovel", "Metal Detector")),
    "Monique Plush":                    LocationInfo("Smoke a cigarette and eat a baguette that's on the ground while sitting", "Misc", rule=HasAll("Lighter", "Cig Pack")),
    "Buried Cacti":                     LocationInfo("Next to the light pole left of Foxtrot", "Misc", enabled=buried, rule=Has("Shovel")),
    "Buried Drive Box":                 LocationInfo("Next to the pole in the grass circle across the river from Alpha Base", "Misc", enabled=buried, rule=Has("Shovel")),
    "Wall Clock":                       LocationInfo("In the Security Booth", "Misc"),
    "Unknown Fruit":                    LocationInfo("At -785.5/-821.7, out of fence", "Misc"),
    **{f"Forest Fuse {i+1}":            LocationInfo("At -331.9/-538.2", "Misc", enabled=fuse) for i in range(4)},

    "Furfur Altar Leg 1":               LocationInfo("In the Antibreather nest, at -671.8/-563.8", "Cave", enabled=time_sensitive),
    "Furfur Altar Leg 2":               LocationInfo("Buried between rocks in Stonehenge at 252.9/585.1", "Stonehenge", enabled=buried, rule=Has("Shovel")),
    "Furfur Altar Top":                 LocationInfo("Buried under the dead tree in the Lake, between 3:00 AM and 4:00 AM", "Lake", enabled=lambda world: buried(world) and time_sensitive(world), rule=HasAll("Shovel", "Scuba Mask", "Scuba Mask Tank")),
    "Furfur Plush":                     LocationInfo("Build the altar and burn a piece of meat under it", "Misc", enabled=furfur_plush_enabled, rule=HasAll("Furfur Altar Leg 1", "Furfur Altar Leg 2", "Furfur Altar Top", "Lighter", "Ritual Knife")),

    "Alpha Server Sandwich":            LocationInfo("", "Alpha Base", enabled=chicken_sandwich),
    "Bathroom Sandwich":                LocationInfo("", "Alpha Base", enabled=chicken_sandwich),
    "Oven Sandwich":                    LocationInfo("", "Alpha Base", enabled=chicken_sandwich),
    "Basement Stairs Sandwich":         LocationInfo("", "Alpha Base", enabled=chicken_sandwich, rule=Has("Crowbar")),
    "Garage Roof Sandwich":             LocationInfo("", "Alpha Base", enabled=chicken_sandwich),
    "Ventilation Unit Sandwich":        LocationInfo("", "Alpha Base", enabled=chicken_sandwich),
    "Radar Dome Sandwich":              LocationInfo("", "Alpha Base", enabled=chicken_sandwich, rule=Has("Half Hook")),
    "Radio Tower Pole Sandwich":        LocationInfo("", "Alpha Base", enabled=chicken_sandwich, rule=Has("Half Hook")),
    "River Sandwich":                   LocationInfo("Under the bridge next to Alpha Base", "Alpha Base", enabled=chicken_sandwich),
    "TR2 Sandwich":                     LocationInfo("On the roof, behind the high voltage box", "TR2", enabled=chicken_sandwich),
    "Lake Log Sandwich":                LocationInfo("Under the rocks", "Lake", enabled=chicken_sandwich),
    "Buried Sandwich":                  LocationInfo("At 157.0/-584.3, near the danger sign", "Misc", enabled=lambda world: buried(world) and chicken_sandwich(world), rule=HasAll("Shovel", "Metal Detector")),
    "Juliett Sandwich":                 LocationInfo("", "Misc", enabled=chicken_sandwich),
    "Whiskey Sandwich":                 LocationInfo("Behind the rocks nearby", "Misc", enabled=chicken_sandwich),
    "Stonehenge Sandwich":              LocationInfo("", "Stonehenge", enabled=chicken_sandwich),
    "Abandoned Shack Sandwich":         LocationInfo("", "Abandoned Shack", enabled=chicken_sandwich),
    "Rozital Ship Sandwich":            LocationInfo("", "Misc", enabled=chicken_sandwich),
    "Fenced Trees Sandwich":            LocationInfo("", "Misc", enabled=chicken_sandwich),
    "Hole Sandwich":                    LocationInfo("", "The Hole", enabled=chicken_sandwich),
    "Cave Entrance Sandwich":           LocationInfo("", "Cave", enabled=chicken_sandwich),
    "Cave Mushroom Pile Sandwich":      LocationInfo("", "Cave", enabled=lambda world: time_sensitive(world) and chicken_sandwich(world)),

    "Bowtie 1":                         LocationInfo("In the New Trees area", "Misc"),
    "Bowtie 2":                         LocationInfo("In the New Trees area", "Misc"),
    "Glasses 1":                        LocationInfo("At the Green Hatch", "Misc"),
    "Glasses 2":                        LocationInfo("At the Green Hatch", "Misc"),
    "Badge 1":                          LocationInfo("At the Hole", "The Hole"),
    "Badge 2":                          LocationInfo("At the Hole", "The Hole"),
    "Jacket 1":                         LocationInfo("At the Hole", "The Hole"),
    "Jacket 2":                         LocationInfo("At the Hole", "The Hole"),

    "Earth Tablet":                     LocationInfo("Within the New Trees area", "Misc", enabled=buried, rule=Has("Shovel")),
    "Water Tablet":                     LocationInfo("In the Lake, beneath the tree", "Lake", enabled=buried, rule=HasAll("Shovel", "Scuba Mask", "Scuba Mask Tank")),
    "Air Tablet":                       LocationInfo("Atop the utility pole closest to TR1", "TR1", rule=Has("Half Hook")),
    "Fire Tablet":                      LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", enabled=lambda world: buried(world) and time_sensitive(world), rule=Has("Shovel")),

    "Maxwell":                          LocationInfo("Type maxwell in a console, then listen for the music", "Misc", enabled=funny),
    "Argemwell":                        LocationInfo("Type argemwell in a console, then listen for the music", "Misc", enabled=funny),
    "Gnarpwell":                        LocationInfo("Type gnarpwell in a console, then listen for the music", "Misc", enabled=funny),
    "Eriewell":                         LocationInfo("Type eriewell in a console, then listen for the music", "Misc", enabled=funny),
    "Thiccfus Plush":                   LocationInfo("Type gooseworx.rufus in a console, then defeat it", "Misc", enabled=funny),
    "Llama Plush":                      LocationInfo("Type llama.saatana in a console, then look for it nearby", "Misc", enabled=funny),
    "Maid Outfit":                      LocationInfo("Buried near the light post on the last turn to TR3", "Misc", enabled=lambda world: funny(world) and buried(world), rule=Has("Shovel")),

    **{f"Survive Day {i+1}":            LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < (world.options.survive_day.value if world.options.objective.value == VOTVGoal.SURVIVE else world.options.survive_days_locations.value),
        rule=Has("Day", i, options=[OptionFilter(DayAsItems, True)], filtered_resolution=True),
        world_item_tier=WorldItems.option_none
    ) for i in range(max_days)},
    **{f"Sell Level {j} Signal {i+1}":  LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < world.options.signal_locations.value,
        rule=Has("Progressive Processing Level", j, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True),
        world_item_tier=WorldItems.option_none
    ) for j in range(4) for i in range(max_signal_locations)},
    **{f"Daily Task Done {i+1}":        LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.daily_task_locations.value, world_item_tier=WorldItems.option_none) for i in range(max_daily_tasks_locations)},
    **{f"Repair Server {i+1}":          LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.server_repair_locations.value, world_item_tier=WorldItems.option_none) for i in range(max_server_repair_locations)},
    **{f"Repair Transformer {i+1}":     LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.transformer_repair_locations.value, world_item_tier=WorldItems.option_none) for i in range(max_transformer_repair_locations)},
    **{f"Replace Fuse {i+1}":           LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.fuse_replacement_locations.value, world_item_tier=WorldItems.option_none, rule=Has("Fuse", count=min(i+1, 10))) for i in range(max_fuse_replacement_locations)},
    **{f"Sell 24 Full Trash Bags {i+1}": LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.trash_bags_locations.value, world_item_tier=WorldItems.option_none) for i in range(max_trash_cleaning_locations)},
    **{f"Light the {dir} Candle":       LocationInfo("", "Tasks", enabled=candles, rule=Has("Lighter"), world_item_tier=WorldItems.option_none) for dir in ('North', 'Northwest', 'West', 'Southwest', 'South', 'Southeast', 'East', 'Northeast')},

    "Repair the Oven":                  LocationInfo("", "Alpha Base", enabled=maintenance, world_item_tier=WorldItems.option_none),
    "Clean the Toilet":                 LocationInfo("", "Alpha Base", enabled=maintenance, world_item_tier=WorldItems.option_none),
    "Clean the Sink":                   LocationInfo("", "Alpha Base", enabled=maintenance, world_item_tier=WorldItems.option_none),
    "Clean the Shower":                 LocationInfo("", "Alpha Base", enabled=maintenance, world_item_tier=WorldItems.option_none),
    "Bake Cookies":                     LocationInfo("", "Alpha Base", enabled=cooking, world_item_tier=WorldItems.option_none),
    "Bake Bread":                       LocationInfo("", "Alpha Base", enabled=cooking, world_item_tier=WorldItems.option_none),
    "Bake a Pizza":                     LocationInfo("", "Alpha Base", enabled=cooking, world_item_tier=WorldItems.option_none),

    **{f"Ball Joints Box {i+1}":        LocationInfo("In the gravel pile near Romeo", "Misc", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=buried), rule=HasAll("Shovel", "Metal Detector")) for i in range(6)},
    **{f"TR{i+1} Limb Joints {j+1}":    LocationInfo("", f"TR{i+1}", enabled=goal({VOTVGoal.KERFUR_OMEGA})) for i in range(3) for j in range(2)},
    "Radioactive Capsule Blueprint":    LocationInfo("At the Green Hatch", "Green Hatch", enabled=goal({VOTVGoal.KERFUR_OMEGA})),
    "TR1 Gas Welder 1":                 LocationInfo("", "TR1", enabled=goal({VOTVGoal.KERFUR_OMEGA})),
    "TR1 Gas Welder 2":                 LocationInfo("", "TR1", enabled=goal({VOTVGoal.KERFUR_OMEGA})),
    "Hole Gas Welder":                  LocationInfo("", "The Hole", enabled=goal({VOTVGoal.KERFUR_OMEGA})),

    "Bunker Keycard":                   LocationInfo("Hookable from the slot at the back of the bunker", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}), rule=HasAny("Bunker Keycard", "Half Hook")),
    "Kerfur-Omega Complete Manual":     LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}), rule=HasAll("Bunker Keycard", "Crowbar")),
    "Kerfur-Omega Documents Binder":    LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}), rule=HasAll("Bunker Keycard", "Crowbar")),

    "Pickaxe":                          LocationInfo("", "Lake", enabled=goal({VOTVGoal.KERFUR_OMEGA}), rule=HasAll("Scuba Mask", "Scuba Mask Tank")),
    "Omega AI Module":                  LocationInfo("", "Lake", enabled=goal({VOTVGoal.KERFUR_OMEGA}), rule=HasAll("Scuba Mask", "Scuba Mask Tank") & HasAny("Half Hook", "Hacksaw")),

    "Buried Radioactive Capsule":       LocationInfo("", "TR2", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=buried), rule=Has("Shovel")),
    "Crafted Radioactive Capsule":      LocationInfo("", "Misc", enabled=lambda world: bool(world.options.enable_crafted_capsule.value) and goal({VOTVGoal.KERFUR_OMEGA})(world), rule=HasAll("Hazmat Suit", "Gas Welder", "Radioactive Capsule Blueprint") & HasAny("Pickaxe", "Hacksaw")),

    "Basement Skull":                   LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH})),
    "Buried Box Skull":                 LocationInfo("At 263.25/-7.25", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}), rule=Has("Shovel")),
    "Gravel Circle Skull":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH})),
    "Radioactive Capsule Skull":        LocationInfo("", "TR2", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH})),
    "Cave Entrance Skull":              LocationInfo("", "Cave", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH})),
    "Stonehenge Skull":                 LocationInfo("", "Stonehenge", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH})),
    "Rozital Ship Skull":               LocationInfo("", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}), rule=HasAll("Lifecrystal Signal", "Shovel") & Has("Progressive Processing Level", 3, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True)),

    "Fire Rune":                        LocationInfo("Explode a rock, violently", "Misc", enabled=goal({VOTVGoal.LAMBERT_PLUSH})),
    "Earth Rune":                       LocationInfo("Bury a rock in the big log near TR2 and dig it up between 0:00 and 1:00", "Misc", enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=lambda world: buried(world) and time_sensitive(world)), rule=Has("Shovel")),
    "Water Rune":                       LocationInfo("Send a rock off the map in the river near the Lake and catch it on the other side", "Misc", enabled=goal({VOTVGoal.LAMBERT_PLUSH})),
    "Air Rune":                         LocationInfo("Send a rock to the top of the map with balloons", "Misc", enabled=goal({VOTVGoal.LAMBERT_PLUSH}), rule=Has("Balloon Pack (WIP)")),
    "Ritual Knife":                     LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=time_sensitive)),

    "Red Argemia Plush":                LocationInfo("In the hole near the estuary of the river in the top right", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb))),
    "Blue Argemia Plush":               LocationInfo("In the river between the first two bridges when walking towards the base", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb))),
    "Green Argemia Plush":              LocationInfo("At the top of the mountain in the bottom left, out of fence", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb)), rule=HasAny("Hiking Boots", "Half Hook")),
    "Yellow Argemia Plush":             LocationInfo("Place a shrimp pack at each corner of the map and in the basement, then look up and away after midnight", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), rule=Has("Shrimp Pack", 5)),
    "Cyan Argemia Plush":               LocationInfo("Put 12 shrimp packs in the emergency shower, and explode them", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), rule=Has("Shrimp Pack", 12)),
    "Magenta Argemia Plush":            LocationInfo("At the Rozital Ship after the lifecrystal signal is processed", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), rule=Has("Lifecrystal Signal")),
    "Nuclear Pink Argemia Plush":       LocationInfo("Near the radio tower at 35.23/-37.24, invisible until bumped", "Misc", enabled=argemia_plush(ArgemiaPlushes.option_all)),
    "Nuclear Yellow Argemia Plush":     LocationInfo("At -634.14/181.37", "Misc", enabled=lambda world: buried(world) and argemia_plush(ArgemiaPlushes.option_all)(world), rule=HasAll("Shovel", "Metal Detector")),
    "Nuclear Orange Argemia Plush":     LocationInfo("Next to the barrier at 872.25/-793.0, high in the sky", "Misc", enabled=argemia_plush(ArgemiaPlushes.option_all), rule=Has("Half Hook")),

    "Alpha Roof Tile":                  LocationInfo("Above the living quarters", "Alpha Base", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "Alpha Bridge Tile":                LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "Xray Tile":                        LocationInfo("Above the nearby lightning rod", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET}), rule=Has("Half Hook")),
    "TR2 Tile":                         LocationInfo("At the base of a tree nearby, in the direction of the Radioactive Capsule", "TR2", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "Hole Tile":                        LocationInfo("Behind the rocks", "The Hole", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "CR3 Tile":                         LocationInfo("On the second-to-last floor", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "Sierra Tile":                      LocationInfo("On the right of the server room", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET})),
    "Stolas Church Tile":               LocationInfo("At the very top, in the empty window", "Village", enabled=goal({VOTVGoal.GREEN_CABINET}), rule=Has("Half Hook")),
    "Green Cabinet Tile":               LocationInfo("", "Green Cabinet", enabled=goal({VOTVGoal.GREEN_CABINET})),

    "Kerfur-Omega":                     LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}, final=True), rule=(
        HasFromList("Red Kerfur", "Blue Kerfur", "Pink Kerfur", count=2) & HasAllCounts({"Radioactive Capsule": 1, "Omega AI Module": 1, "Limb Joint": 4, "Ball Joint": 8, "Progressive Camera": 3, "Kerfur-Omega Complete Manual": 1})
        & HasAll(*(f"{x} Scrap Recipe" for x in ("Plastic", "Metal", "Glass", "Electronic")), options=[OptionFilter(ScrapRecipesAsItems, True)], filtered_resolution=True)
    )),
    "Hell Rock":                        LocationInfo("", "Stonehenge", enabled=goal({VOTVGoal.HELL_ROCK}, final=True), rule=HasAllCounts({"Skull": 7})),
    "White Argemia Plush":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH}, final=True), rule=HasAllCounts({"Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Black Argemia Plush":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.BLACK_ARGEMIA_PLUSH}, final=True), rule=HasAllCounts({"Skull": 7, "Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Lambert Plush":                    LocationInfo("", "Abandoned Shack", enabled=goal({VOTVGoal.LAMBERT_PLUSH}, final=True), rule=HasAllCounts({"Fire Rune": 1, "Earth Rune": 1, "Water Rune": 1, "Air Rune": 1, "Ritual Knife": 1})),
    "Open the Green Cabinet":           LocationInfo("", "Green Cabinet", enabled=goal({VOTVGoal.GREEN_CABINET}, final=True), rule=HasAllCounts({"Tile": 9})),
}
