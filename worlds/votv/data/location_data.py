from typing import NamedTuple

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAllCounts, HasAny, HasFromList, Rule

from ..Options import DayAsItems, ScrapRecipesAsItems, UpgradesAsItems
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

class LocationInfo(NamedTuple):
    hint: str
    group: str
    category: list[str]
    goals: set[VOTVGoal] = set()
    rule: Rule | None = None
    is_buried: bool = False
    radioactive_capsule_craft_required: bool = False
    maintenance_task: bool = False
    cooking_task: bool = False
    is_time_sensitive: bool = False
    is_funny: bool = False
    is_final: bool = False

locations = {
    "Spectogram Module":                LocationInfo("In a drawer in the basement", "Alpha Base", ["Misc"]),
    "Medkit":                           LocationInfo("In the Administration Office", "Alpha Base", ["Misc"]),
    "Car Keys":                         LocationInfo("In the Administration Office", "Alpha Base", ["Misc"]),
    "Cooking Book":                     LocationInfo("In the living quarters", "Alpha Base", ["Misc"]),
    # Disabled because it requires a specific event that might be skipped
    # "Lead Pipe":                        LocationInfo("In the first vent above when entering the Signal Room", ["Tools"], rule=Has("Half Hook")),
    "Miniature Gas Can":                LocationInfo("On top of the garage in a corner", "Alpha Base", ["Misc"]),
    "Alpha Toolbox":                    LocationInfo("", "Alpha Base", ["Tools"]),

    **{f"TR{i+1} Watering Can":         LocationInfo("", f"TR{i+1}", ["Misc"]) for i in range(3)},
    "TR1 Cigarettes":                   LocationInfo("", "TR1", ["Misc"]),
    "TR1 Tinfoil Hat":                  LocationInfo("", "TR1", ["Misc"]),
    "TR1 Toolbox":                      LocationInfo("", "TR1", ["Tools"]),
    "TR1 Lighter":                      LocationInfo("", "TR1", ["Tools"]),
    "TR2 Car Battery Charger":          LocationInfo("", "TR2", ["Tools"]),
    "TR2 Shovel":                       LocationInfo("In the rafters", "TR2", ["Tools"]),
    "TR3 Hiking Boots":                 LocationInfo("", "TR3", ["Tools"]),

    "Hole Toolbox":                     LocationInfo("", "The Hole", ["Tools"]),
    "EMF Detector":                     LocationInfo("At the Hole, near a fallen construction light", "The Hole", ["Tools"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Lantern":                          LocationInfo("At the Hole", "The Hole", ["Tools"]),

    "Green Hatch Toolbox":              LocationInfo("", "Green Hatch", ["Tools"]),
    "Geiger Counter":                   LocationInfo("At the Green Hatch", "Green Hatch", ["Tools"]),

    "Abandoned Shack Shovel":           LocationInfo("", "Abandoned Shack", ["Tools"]),
    "Axe":                              LocationInfo("At the Abandoned Shack", "Abandoned Shack", ["Tools"]),
    "Deer Skull":                       LocationInfo("In the Abandoned Shack", "Abandoned Shack", ["Misc"]),
    "Seed Pack (The Thingy)":           LocationInfo("At the Abandoned Shack", "Abandoned Shack", ["Misc"]),

    "Stonehenge Shovel":                LocationInfo("", "Stonehenge", ["Tools"]),
    "Security Booth Shovel":            LocationInfo("", "Misc", ["Tools"]),
    "Bike Helmet":                      LocationInfo("On top of the rocks to the right of the security booth", "Misc", ["Tools"]),
    "Old Rifle":                        LocationInfo("In Lima's server room", "Misc", ["Misc"]),
    "Fisherman's Treasure":             LocationInfo("At 176.06/-460.41", "Misc", ["Misc"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Well Hook 1":                      LocationInfo("", "Misc", ["Tools"], rule=Has("Half Hook")),
    "Well Hook 2":                      LocationInfo("", "Misc", ["Tools"], rule=Has("Half Hook")),
    "Argemia Mug":                      LocationInfo("Atop the utility pole closest to the windmills", "Misc", ["Misc"], rule=Has("Half Hook")),
    "Limestone Slab":                   LocationInfo("At 567.0/237.0 near the treehouse", "Misc", ["Misc"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Green Fire Rock":                  LocationInfo("Extinguish the green fire in the Village (Day 8+, from 0:00 to 1:00)", "Misc", ["Village"], is_time_sensitive=True),
    "Antibreather Plush":               LocationInfo("In the Cave, at 3:33 AM", "Cave", ["Plushes"], is_time_sensitive=True),
    "Erie Plush":                       LocationInfo("Bury a meat garbage bag at Sierra", "Misc", ["Plushes"], is_buried=True, rule=Has("Shovel"), is_time_sensitive=True),
    "Librarian Candle":                 LocationInfo("In the log under the lake surface", "Lake", ["Plushes"], is_buried=True, rule=Has("Shovel")),
    "Dream Plush":                      LocationInfo("Buried near the south side of the Lake", "Lake", ["Plushes"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Monique Plush":                    LocationInfo("Smoke a cigarette and eat a baguette that's on the ground while sitting", "Misc", ["Plushes"], rule=HasAll("Lighter", "Cig Pack")),

    "Alpha Server Sandwich":            LocationInfo("Above the servers", "Alpha Base", ["Chicken Sandwiches"]),
    "Bathroom Sandwich":                LocationInfo("", "Alpha Base", ["Chicken Sandwiches"]),
    "Oven Sandwich":                    LocationInfo("", "Alpha Base", ["Chicken Sandwiches"]),
    "Basement Stairs Sandwich":         LocationInfo("", "Alpha Base", ["Chicken Sandwiches"], rule=Has("Crowbar")),
    "Garage Roof Sandwich":             LocationInfo("", "Alpha Base", ["Chicken Sandwiches"]),
    "Ventilation Unit Sandwich":        LocationInfo("", "Alpha Base", ["Chicken Sandwiches"]),
    "Radar Dome Sandwich":              LocationInfo("", "Alpha Base", ["Chicken Sandwiches"], rule=Has("Half Hook")),
    "Radio Tower Pole Sandwich":        LocationInfo("", "Alpha Base", ["Chicken Sandwiches"], rule=Has("Half Hook")),
    "River Sandwich":                   LocationInfo("Under the bridge next to Alpha Base", "Alpha Base", ["Chicken Sandwiches"]),
    "TR2 Sandwich":                     LocationInfo("On the roof, behind the high voltage box", "TR2", ["Chicken Sandwiches"]),
    "Lake Log Sandwich":                LocationInfo("Under the rocks", "Lake", ["Chicken Sandwiches"]),
    "Buried Sandwich":                  LocationInfo("At 157.0/-584.3", "Misc", ["Chicken Sandwiches"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Juliett Sandwich":                 LocationInfo("", "Misc", ["Chicken Sandwiches"]),
    "Whiskey Sandwich":                 LocationInfo("Behind the rocks nearby", "Misc", ["Chicken Sandwiches"]),
    "Stonehenge Sandwich":              LocationInfo("", "Stonehenge", ["Chicken Sandwiches"]),
    "Abandoned Shack Sandwich":         LocationInfo("", "Abandoned Shack", ["Chicken Sandwiches"]),
    "Rozital Ship Sandwich":            LocationInfo("", "Misc", ["Chicken Sandwiches"]),
    "Fenced Trees Sandwich":            LocationInfo("", "Misc", ["Chicken Sandwiches"]),
    "Hole Sandwich":                    LocationInfo("", "The Hole", ["Chicken Sandwiches"]),
    "Cave Entrance Sandwich":           LocationInfo("", "Cave", ["Chicken Sandwiches"]),
    "Cave Mushroom Pile Sandwich":      LocationInfo("", "Cave", ["Chicken Sandwiches"], is_time_sensitive=True),

    "Earth Tablet":                     LocationInfo("Within the New Trees area", "Misc", ["Lambert Plush"], is_buried=True, rule=Has("Shovel")),
    "Water Tablet":                     LocationInfo("In the Lake, beneath the tree", "Lake", ["Lambert Plush"], is_buried=True, rule=HasAll("Shovel", "Scuba Mask", "Scuba Mask Tank")),
    "Air Tablet":                       LocationInfo("Atop the utility pole closest to TR1", "TR1", ["Lambert Plush"], rule=Has("Half Hook")),
    "Fire Tablet":                      LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", ["Lambert Plush"], is_time_sensitive=True, is_buried=True, rule=Has("Shovel")),

    **{f"Ball Joints Box {i+1}":        LocationInfo("In the gravel pile near Romeo", "Misc", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, is_buried=True, rule=HasAll("Shovel", "Metal Detector")) for i in range(6)},
    **{f"TR{i+1} Limb Joints {j+1}":    LocationInfo("", f"TR{i+1}", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}) for i in range(3) for j in range(2)},
    "Radioactive Capsule Blueprint":    LocationInfo("", "Green Hatch", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}),
    "TR1 Gas Welder 1":                 LocationInfo("", "TR1", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}),
    "TR1 Gas Welder 2":                 LocationInfo("", "TR1", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}),
    "Hole Gas Welder":                  LocationInfo("", "The Hole", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}),

    "Bunker Keycard":                   LocationInfo("Hookable from the slot at the back of the bunker", "Alpha Base", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, rule=HasAny("Bunker Keycard", "Half Hook")),
    "Kerfur-Omega Complete Manual":     LocationInfo("", "Alpha Base", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, rule=Has("Bunker Keycard")),
    "Kerfur-Omega Documents Binder":    LocationInfo("", "Alpha Base", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, rule=Has("Bunker Keycard")),

    "Pickaxe":                          LocationInfo("", "Lake", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, rule=HasAll("Scuba Mask", "Scuba Mask Tank")),
    "Omega AI Module":                  LocationInfo("", "Lake", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, rule=HasAll("Scuba Mask", "Scuba Mask Tank") & HasAny("Half Hook", "Hacksaw")),

    "Buried Radioactive Capsule":       LocationInfo("", "TR2", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, is_buried=True, rule=Has("Shovel")),
    "Crafted Radioactive Capsule":      LocationInfo("", "Misc", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, radioactive_capsule_craft_required=True, rule=HasAll("Hazmat Suit", "Gas Welder", "Radioactive Capsule Blueprint") & HasAny("Pickaxe", "Hacksaw")),

    "Basement Skull":                   LocationInfo("", "Alpha Base", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}),
    "Buried Box Skull":                 LocationInfo("At 263.25/-7.25", "Misc", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, rule=Has("Shovel")),
    "Gravel Circle Skull":              LocationInfo("", "Misc", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}),
    "Radioactive Capsule Skull":        LocationInfo("", "TR2", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}),
    "Cave Entrance Skull":              LocationInfo("", "Cave", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}),
    "Stonehenge Skull":                 LocationInfo("", "Stonehenge", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}),
    "Rozital Capsule Skull":            LocationInfo("", "Misc", ["Misc"], goals={VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, rule=Has("Lifecrystal Signal") & Has("Progressive Processing Level", 3, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True) & Has("Shovel")),

    "Ritual Knife":                     LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", ["Lambert Plush"], is_time_sensitive=True, goals={VOTVGoal.LAMBERT_PLUSH}),

    "Red Argemia Plush":                LocationInfo("In the hole near the estuary of the river in the top right", "Misc", ["Plushes"]),
    "Blue Argemia Plush":               LocationInfo("In the river between the first two bridges when walking towards the base", "Misc", ["Plushes"]),
    "Green Argemia Plush":              LocationInfo("At the top of the mountain in the bottom left, out of fence", "Misc", ["Plushes"], rule=HasAny("Hiking Boots", "Half Hook")),
    "Yellow Argemia Plush":             LocationInfo("Place a shrimp pack at each corner of the map and in the basement, then look up and away after midnight", "Misc", ["Plushes"], goals={VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, rule=Has("Shrimp Pack", 5)),
    "Cyan Argemia Plush":               LocationInfo("Put 12 shrimp packs in the emergency shower, and explode them", "Misc", ["Plushes"], goals={VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, rule=Has("Shrimp Pack", 12)),
    "Magenta Argemia Plush":            LocationInfo("At the Rozital Capsule after the lifecrystal signal is processed", "Misc", ["Plushes"], goals={VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, rule=Has("Lifecrystal Signal")),

    "Nuclear Pink Argemia Plush":       LocationInfo("Near the radio tower at 35.23/-37.24, invisible until bumped", "Misc", ["Plushes"]),
    "Nuclear Yellow Argemia Plush":     LocationInfo("At -634.14/181.37", "Misc", ["Plushes"], is_buried=True, rule=HasAll("Shovel", "Metal Detector")),
    "Nuclear Orange Argemia Plush":     LocationInfo("Next to the barrier at 872.25/-793.0, high in the sky", "Misc", ["Plushes"], rule=Has("Half Hook")),

    "Alpha Roof Tile":                  LocationInfo("Above the living quarters", "Alpha Base", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "Alpha Bridge Tile":                LocationInfo("", "Alpha Base", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "Xray Tile":                        LocationInfo("Above the nearby lightning rod", "Misc", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}, rule=Has("Half Hook")),
    "TR2 Tile":                         LocationInfo("At the base of a tree nearby, in the direction of the Radioactive Capsule", "TR2", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "Hole Tile":                        LocationInfo("Behind the rocks", "The Hole", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "CR3 Tile":                         LocationInfo("On the second-to-last floor", "Misc", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "Sierra Tile":                      LocationInfo("On the right of the server room", "Misc", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),
    "Stolas Church Tile":               LocationInfo("At the very top, in the empty window", "Village", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}, rule=Has("Half Hook")),
    "Green Cabinet Tile":               LocationInfo("", "Green Cabinet", ["Tiles"], goals={VOTVGoal.GREEN_CABINET}),

    "Maxwell":                          LocationInfo("Type maxwell in a console, then listen for the music", "Misc", ["Funny setting"], is_funny=True),
    "Argemwell":                        LocationInfo("Type argemwell in a console, then listen for the music", "Misc", ["Funny setting"], is_funny=True),
    "Gnarpwell":                        LocationInfo("Type gnarpwell in a console, then listen for the music", "Misc", ["Funny setting"], is_funny=True),
    "Eriewell":                         LocationInfo("Type eriewell in a console, then listen for the music", "Misc", ["Funny setting"], is_funny=True),
    "Thiccfus Plush":                   LocationInfo("Type gooseworx.rufus in a console, then defeat it", "Misc", ["Funny setting"], is_funny=True),
    "Maid Outfit":                      LocationInfo("Buried near the light post on the last turn to TR3", "Misc", ["Funny setting"], is_funny=True, is_buried=True, rule=Has("Shovel")),

    **{f"Survive Day {i+1}":            LocationInfo("", "Tasks", ["Tasks"], rule=Has("Day", i, options=[OptionFilter(DayAsItems, True)], filtered_resolution=True)) for i in range(max_days)},
    **{f"Sell Level {j} Signal {i+1}":  LocationInfo("", "Tasks", ["Tasks"], rule=Has("Progressive Processing Level", j, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True)) for j in range(4) for i in range(max_signal_locations)},
    **{f"Daily Task Done {i+1}":        LocationInfo("", "Tasks", ["Tasks"]) for i in range(max_daily_tasks_locations)},
    **{f"Repair Server {i+1}":          LocationInfo("", "Tasks", ["Tasks"]) for i in range(max_server_repair_locations)},
    **{f"Repair Transformer {i+1}":     LocationInfo("", "Tasks", ["Tasks"]) for i in range(max_transformer_repair_locations)},
    **{f"Replace Fuse {i+1}":           LocationInfo("", "Tasks", ["Tasks"]) for i in range(max_fuse_replacement_locations)},
    **{f"Sell 24 Full Trash Bags {i+1}": LocationInfo("", "Tasks", ["Tasks"]) for i in range(max_trash_cleaning_locations)},

    "Repair the Oven":                  LocationInfo("", "Alpha Base", ["Tasks"], maintenance_task=True),
    "Clean the Toilet":                 LocationInfo("", "Alpha Base", ["Tasks"], maintenance_task=True),
    "Clean the Sink":                   LocationInfo("", "Alpha Base", ["Tasks"], maintenance_task=True),
    "Clean the Shower":                 LocationInfo("", "Alpha Base", ["Tasks"], maintenance_task=True),
    "Bake Cookies":                     LocationInfo("", "Alpha Base", ["Tasks"], cooking_task=True),
    "Bake Bread":                       LocationInfo("", "Alpha Base", ["Tasks"], cooking_task=True),
    "Bake a Pizza":                     LocationInfo("", "Alpha Base", ["Tasks"], cooking_task=True),

    "Kerfur-Omega":                     LocationInfo("", "Alpha Base", ["Kerfur-Omega"], goals={VOTVGoal.KERFUR_OMEGA}, is_final=True, rule=(
        HasFromList("Red Kerfur", "Blue Kerfur", "Pink Kerfur", count=2) & HasAllCounts({"Radioactive Capsule": 1, "Omega AI Module": 1, "Limb Joint": 4, "Ball Joint": 6, "Progressive Camera": 3, "Kerfur-Omega Complete Manual": 1})
        & HasAll(*(f"{x} Scrap Recipe" for x in ("Plastic", "Metal", "Glass", "Electronic")), options=[OptionFilter(ScrapRecipesAsItems, True)], filtered_resolution=True)
    )),
    "Hell Rock":                        LocationInfo("", "Stonehenge", ["Misc"], goals={VOTVGoal.HELL_ROCK}, is_final=True, rule=HasAllCounts({"Skull": 7})),
    "White Argemia Plush":              LocationInfo("", "Misc", ["Plushes"], goals={VOTVGoal.WHITE_ARGEMIA_PLUSH}, is_final=True, rule=HasAllCounts({"Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Black Argemia Plush":              LocationInfo("", "Misc", ["Plushes"], goals={VOTVGoal.BLACK_ARGEMIA_PLUSH}, is_final=True, rule=HasAllCounts({"Skull": 7, "Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Lambert Plush":                    LocationInfo("", "Abandoned Shack", ["Plushes"], goals={VOTVGoal.LAMBERT_PLUSH}, is_final=True, rule=HasAllCounts({"Balloon Pack": 1, "Half Hook": 1, "Ritual Knife": 1})),
    "Open the Green Cabinet":           LocationInfo("", "Green Cabinet", ["Misc"], goals={VOTVGoal.GREEN_CABINET}, is_final=True, rule=HasAllCounts({"Tile": 9})),
}
