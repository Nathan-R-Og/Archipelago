from typing import TYPE_CHECKING, Callable, NamedTuple

from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachRegion, Has, HasAll, HasAllCounts, HasAny, HasFromList, Rule

from ..Utils import CanGetSignals, CanReachPotentialSpawnLocations, DayItemFieldResolver, HasShovel, is_goal_enabled, furfur_plush_enabled, lifecrystal_signal_enabled
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
    region: str = "Outside"
    rule: Rule | None = None
    enabled: "EnabledFunc" = lambda _: True
    complex: bool = False

def goal(goals: set[VOTVGoal], final: bool = False, also: "EnabledFunc" = lambda _: True) -> "EnabledFunc" :
    return lambda world: world.options.objective.value in goals or not final and any(is_goal_enabled(world, x) for x in goals) and also(world)

def argemia_plush(setting: int) -> "EnabledFunc":
    return lambda world: world.options.argemia_plushes.value >= setting

def world_item(setting: int = WorldItems.option_base) -> "EnabledFunc":
    return lambda world: world.options.world_items.value >= setting

def buried(world: "VOTVWorld"):
    return bool(world.options.buried_items.value)

def time_sensitive(world: "VOTVWorld"):
    return bool(world.options.time_sensitive.value)

def funny(world: "VOTVWorld"):
    return bool(world.options.funny_setting.value)

def maintenance(world: "VOTVWorld"):
    return bool(world.options.maintenance_tasks.value)

def cooking(world: "VOTVWorld"):
    return bool(world.options.cooking_tasks.value)

def candles(world: "VOTVWorld"):
    return bool(world.options.rock_candles.value)

def fuse(world: "VOTVWorld"):
    return world.options.fuse_replacement_locations.value > 0

def _and(*args: "EnabledFunc") -> "EnabledFunc":
    def _and(world):
        for comp in args:
            if not comp(world):
                return False
        return True
    return _and

locations = {
    "Spectogram Module":                LocationInfo("In a drawer in the basement", "Alpha Base", region="Alpha Stairs", enabled=world_item()),
    "Medkit":                           LocationInfo("In the Administration Office", "Alpha Base", region="Admin Room", enabled=world_item()),
    "Car Keys":                         LocationInfo("In the Administration Office", "Alpha Base", region="Admin Room", enabled=world_item()),
    "Cooking Book":                     LocationInfo("In the living quarters", "Alpha Base", region="Staff Room", enabled=world_item()),
    # Disabled because it requires a specific event that might be skipped
    # "Lead Pipe":                        LocationInfo("In the first vent above when entering the Signal Room", region="Signal Lab", rule=HasAny("Half Hook", "Hook")),
    "Miniature Gas Can":                LocationInfo("On top of the garage in a corner", "Alpha Base", region="Alpha Roof", enabled=world_item(WorldItems.option_hidden)),
    **{f"Garage Gas Can {i+1}":         LocationInfo("", "Alpha Base", region="Garage", enabled=world_item()) for i in range(3)},
    "Alpha Toolbox":                    LocationInfo("", "Alpha Base", region="Garage", enabled=world_item()),
    "ATV Wheel":                        LocationInfo("", "Alpha Base", region="Garage", enabled=world_item()),
    "Ammo Box":                         LocationInfo("Behind the crates in the garage", "Alpha Base", region="Garage", enabled=world_item(WorldItems.option_hidden)),
    "Alpha Broom":                      LocationInfo("In the utility closet", "Alpha Base", region="Utility Closet", enabled=world_item()),
    "Utility Closet Gas Can":           LocationInfo("", "Alpha Base", region="Utility Closet", enabled=world_item()),
    "Pipebomb":                         LocationInfo("In the corner drawer in the signal room", "Alpha Base", region="Signal Lab", enabled=world_item(WorldItems.option_hidden)),
    "Sponge":                           LocationInfo("In the signal room", "Alpha Base", enabled=_and(maintenance, world_item()), region="Signal Lab"),
    "Signal Lab Gas Can":               LocationInfo("", "Alpha Base", region="Signal Lab", enabled=world_item()),
    **{f"Alpha Fuse {i+1}":             LocationInfo("In the upstairs storage room", "Alpha Base", enabled=_and(fuse, world_item()), region="Storage Room") for i in range(3)},
    "Substation Gas Can":               LocationInfo("", "Alpha Base", enabled=world_item()),

    **{f"TR{i+1} Watering Can":         LocationInfo("", f"TR{i+1}", region="Outside" if i != 2 else f"TR{i+1} Room", enabled=world_item(WorldItems.option_hidden if i == 1 else WorldItems.option_base)) for i in range(3)},
    **{f"TR{i+1} Fuse":                 LocationInfo("", f"TR{i+1}", enabled=_and(fuse, world_item()), region="Outside" if i == 0 else f"TR{i+1} Room") for i in range(3)},
    **{f"TR{i+1} Gas Can {k+1}":        LocationInfo("", f"TR{i+1}", region="Outside" if i == 0 or i == 1 and k < 2 else f"TR{i+1} Room", enabled=world_item()) for i, j in enumerate((5, 4, 1)) for k in range(j)},
    "TR1 Toolbox":                      LocationInfo("", "TR1", enabled=world_item()),
    "TR1 Cigarettes":                   LocationInfo("", "TR1", region="TR1 Room", enabled=world_item()),
    "TR1 Tinfoil Hat":                  LocationInfo("", "TR1", region="TR1 Room", enabled=world_item()),
    "TR1 Lighter":                      LocationInfo("", "TR1", region="TR1 Room", enabled=world_item()),
    "TR1 Broom":                        LocationInfo("", "TR1", region="TR1 Room", enabled=world_item()),
    "TR2 Car Battery Charger":          LocationInfo("", "TR2", region="TR2 Room", enabled=world_item()),
    "TR2 Shovel":                       LocationInfo("In the rafters", "TR2", enabled=world_item(WorldItems.option_hidden)),
    "TR3 Hiking Boots":                 LocationInfo("", "TR3", region="TR3 Room", enabled=world_item()),

    "Hole Toolbox":                     LocationInfo("", "The Hole", enabled=world_item()),
    **{f"Hole Gas Can {i+1}":           LocationInfo("", "The Hole", enabled=world_item()) for i in range(2)},
    "EMF Detector":                     LocationInfo("At the Hole, near a fallen construction light", "The Hole", enabled=_and(buried,world_item(WorldItems.option_extreme)), rule=HasShovel() & Has("Metal Detector")),
    # "Lantern":                          LocationInfo("At the Hole", "The Hole"),  # Disabled for randomizing its key
    "Hole Welding Mask":                LocationInfo("", "The Hole", enabled=world_item()),

    "Green Hatch Toolbox":              LocationInfo("", "Green Hatch", region="Green Hatch", enabled=world_item()),
    "Geiger Counter":                   LocationInfo("At the Green Hatch", "Green Hatch", region="Green Hatch", enabled=world_item()),
    "Green Hatch Welding Mask":         LocationInfo("", "Green Hatch", region="Green Hatch", enabled=world_item()),

    "Abandoned Shack Shovel":           LocationInfo("", "Abandoned Shack", region="Abandoned Shack", enabled=world_item()),
    "Axe":                              LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item(WorldItems.option_hidden)),
    "Deer Skull":                       LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item(WorldItems.option_hidden)),
    "Boar Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item()),
    "Deer Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item()),
    "Goat Trophy Head":                 LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item()),
    "Seed Pack (The Thingy)":           LocationInfo("In the Abandoned Shack", "Abandoned Shack", region="Abandoned Shack", enabled=world_item(WorldItems.option_hidden)),

    "Extinguish the Green Fire":        LocationInfo("In the Village, Day 8+, from 12:00 AM to 1:00 AM", "Village", complex=True, enabled=time_sensitive, region="Restricted Area", rule=Has("Day", DayItemFieldResolver(7), options=[OptionFilter(DayAsItems, True)], filtered_resolution=True)),
    "Compost Bucket 1":                 LocationInfo("In the Village's farm plot", "Village", region="Restricted Area", enabled=world_item(WorldItems.option_hidden)),
    "Compost Bucket 2":                 LocationInfo("In the Village's farm plot", "Village", region="Restricted Area", enabled=world_item(WorldItems.option_hidden)),

    "Stonehenge Shovel":                LocationInfo("", "Stonehenge", region="Stonehenge", enabled=world_item()),
    "Security Booth Shovel":            LocationInfo("", "Misc", enabled=world_item()),
    "Bike Helmet":                      LocationInfo("On top of the rocks to the right of the security booth", "Misc", enabled=world_item(WorldItems.option_hidden)),
    "Old Rifle":                        LocationInfo("In Lima's server room", "Misc", enabled=world_item()),
    "Fisherman's Treasure":             LocationInfo("At 176.06/-460.41", "Misc", enabled=_and(buried, world_item(WorldItems.option_hidden)), rule=HasShovel() & Has("Metal Detector")),
    "Well Hook 1":                      LocationInfo("", "Misc", rule=HasAny("Half Hook", "Hook"), enabled=world_item(WorldItems.option_hidden)),
    "Well Hook 2":                      LocationInfo("", "Misc", rule=HasAny("Half Hook", "Hook"), enabled=world_item(WorldItems.option_hidden)),
    "Jar of Honey":                     LocationInfo("Atop the second utility pole from TR3", "Misc", rule=HasAny("Half Hook", "Hook"), enabled=world_item(WorldItems.option_extreme)),
    "Argemia Mug":                      LocationInfo("Atop the utility pole closest to the windmills", "Misc", rule=HasAny("Half Hook", "Hook"), enabled=world_item(WorldItems.option_extreme)),
    "Limestone Slab":                   LocationInfo("At 567.0/237.0 near the treehouse", "Misc", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel() & Has("Metal Detector")),
    "Antibreather Plush":               LocationInfo("Be in the Cave at 3:33 AM, then look in the larger nest", "Cave", complex=True, enabled=_and(time_sensitive, world_item(WorldItems.option_extreme)), region="Cave"),
    "Erie Plush":                       LocationInfo("Bury a meat garbage bag at Sierra and wait for 1:00 AM", "Misc", complex=True, enabled=_and(buried, time_sensitive, world_item(WorldItems.option_extreme)), rule=HasShovel() & CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs")),
    "Librarian Candle":                 LocationInfo("In the log under the lake surface", "Lake", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel()),
    "Dream Plush":                      LocationInfo("Buried near the bottom side of the Lake", "Lake", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel() & Has("Metal Detector")),
    "Monique Plush":                    LocationInfo("Smoke a cigarette and eat a baguette that's on the ground while sitting", "Misc", rule=Has("Cig Pack") & CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs"), enabled=world_item(WorldItems.option_extreme)),
    "Buried Cacti":                     LocationInfo("Next to the light pole left of Foxtrot", "Misc", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel()),
    "Buried Drive Box":                 LocationInfo("Next to the pole in the grass circle across the river from Alpha Base", "Misc", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel()),
    "Wall Clock":                       LocationInfo("In the Security Booth", "Misc", enabled=world_item()),
    "Unknown Fruit":                    LocationInfo("At -785.5/-821.7, out of fence", "Misc", rule=CanReachRegion("Garage") & Has("Gas Can"), enabled=world_item(WorldItems.option_extreme)),  # Not strictly necessary but better with the ATV
    **{f"Forest Fuse {i+1}":            LocationInfo("At -331.9/-538.2", "Misc", enabled=_and(fuse, world_item(WorldItems.option_hidden))) for i in range(4)},

    "Furfur Altar Leg 1":               LocationInfo("In the Antibreather nest, at -671.8/-563.8", "Cave", enabled=_and(time_sensitive, world_item(WorldItems.option_extreme)), region="Cave"),
    "Furfur Altar Leg 2":               LocationInfo("Buried between rocks in Stonehenge at 252.9/585.1", "Stonehenge", enabled=_and(buried, world_item(WorldItems.option_extreme)), region="Stonehenge", rule=HasShovel()),
    "Furfur Altar Top":                 LocationInfo("Buried under the dead tree in the Lake, between 3:00 AM and 4:00 AM", "Lake", region="Lake", enabled=_and(buried, time_sensitive, world_item(WorldItems.option_extreme)), rule=HasShovel()),
    "Furfur Plush":                     LocationInfo("Build the altar and burn a piece of meat under it", "Misc", complex=True, enabled=furfur_plush_enabled, rule=HasAll("Furfur Altar Leg 1", "Furfur Altar Leg 2", "Furfur Altar Top", "Lighter", "Ritual Knife")),

    "Alpha Server Sandwich":            LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_hidden), region="Server Room"),
    "Bathroom Sandwich":                LocationInfo("", "Alpha Base", enabled=world_item(), region="Bathroom"),
    "Oven Sandwich":                    LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_hidden), region="Staff Room"),
    "Basement Stairs Sandwich":         LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_hidden), region="Alpha Stairs", rule=Has("Crowbar")),
    "Garage Roof Sandwich":             LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_hidden), region="Alpha Roof"),
    "Ventilation Unit Sandwich":        LocationInfo("", "Alpha Base", enabled=world_item(), region="Alpha Roof"),
    "Radar Dome Sandwich":              LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_hidden), region="Alpha Roof", rule=HasAny("Half Hook", "Hook")),
    "Radio Tower Pole Sandwich":        LocationInfo("", "Alpha Base", enabled=world_item(WorldItems.option_extreme), rule=HasAny("Half Hook", "Hook")),
    "River Sandwich":                   LocationInfo("Under the bridge next to Alpha Base", "Alpha Base", enabled=world_item(WorldItems.option_hidden)),
    "TR2 Sandwich":                     LocationInfo("On the roof, behind the high voltage box", "TR2", enabled=world_item(WorldItems.option_hidden)),
    "Lake Log Sandwich":                LocationInfo("Under the rocks", "Lake", enabled=world_item(WorldItems.option_hidden)),
    "Buried Sandwich":                  LocationInfo("At 157.0/-584.3, near the danger sign", "Misc", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel() & Has("Metal Detector")),
    "Juliett Sandwich":                 LocationInfo("", "Misc", enabled=world_item(WorldItems.option_hidden)),
    "Whiskey Sandwich":                 LocationInfo("Behind the rocks nearby", "Misc", enabled=world_item(WorldItems.option_hidden)),
    "Stonehenge Sandwich":              LocationInfo("", "Stonehenge", enabled=world_item(WorldItems.option_hidden), region="Stonehenge"),
    "Abandoned Shack Sandwich":         LocationInfo("", "Abandoned Shack", enabled=world_item()),
    "Rozital Ship Sandwich":            LocationInfo("", "Misc", enabled=world_item()),
    "Fenced Trees Sandwich":            LocationInfo("", "Misc", enabled=world_item(), region="New Trees Area"),
    "Hole Sandwich":                    LocationInfo("", "The Hole", enabled=world_item()),
    "Cave Entrance Sandwich":           LocationInfo("", "Cave", enabled=world_item()),
    "Cave Mushroom Pile Sandwich":      LocationInfo("", "Cave", enabled=_and(time_sensitive, world_item(WorldItems.option_hidden)), complex=True, region="Cave"),

    "Bowtie 1":                         LocationInfo("In the New Trees area", "Misc", region="New Trees Area", enabled=world_item()),
    "Bowtie 2":                         LocationInfo("In the New Trees area", "Misc", region="New Trees Area", enabled=world_item()),
    "Glasses 1":                        LocationInfo("At the Green Hatch", "Green Hatch", region="Green Hatch", enabled=world_item()),
    "Glasses 2":                        LocationInfo("At the Green Hatch", "Green Hatch", region="Green Hatch", enabled=world_item()),
    "Badge 1":                          LocationInfo("At the Hole", "The Hole", enabled=world_item()),
    "Badge 2":                          LocationInfo("At the Hole", "The Hole", enabled=world_item()),
    "Jacket 1":                         LocationInfo("At the Hole", "The Hole", enabled=world_item()),
    "Jacket 2":                         LocationInfo("At the Hole", "The Hole", enabled=world_item()),

    "Earth Tablet":                     LocationInfo("Within the New Trees area", "Misc", enabled=_and(buried, world_item(WorldItems.option_extreme)), rule=HasShovel() & HasAny("Digital Map", "Metal Detector")),
    "Water Tablet":                     LocationInfo("In the Lake, beneath the tree", "Lake", enabled=_and(buried, world_item(WorldItems.option_extreme)), region="Lake", rule=HasShovel()),
    "Air Tablet":                       LocationInfo("Atop the utility pole closest to TR1", "TR1", rule=HasAny("Half Hook", "Hook"), enabled=world_item(WorldItems.option_extreme)),
    "Fire Tablet":                      LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", enabled=_and(buried, time_sensitive, world_item(WorldItems.option_extreme)), rule=HasShovel()),

    "Maxwell":                          LocationInfo("Type maxwell in a console, then listen for the music", "Misc", enabled=funny, rule=CanReachPotentialSpawnLocations()),
    "Argemwell":                        LocationInfo("Type argemwell in a console, then listen for the music", "Misc", enabled=funny, rule=CanReachPotentialSpawnLocations()),
    "Gnarpwell":                        LocationInfo("Type gnarpwell in a console, then listen for the music", "Misc", enabled=funny, rule=CanReachPotentialSpawnLocations()),
    "Eriewell":                         LocationInfo("Type eriewell in a console, then listen for the music", "Misc", enabled=funny, rule=CanReachPotentialSpawnLocations()),
    "Thiccfus Plush":                   LocationInfo("Type gooseworx.rufus in a console, then defeat it", "Misc", enabled=funny, rule=Has("Gas Can", options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True)),
    "Llama Plush":                      LocationInfo("Type llama.saatana in a console, then look for it nearby", "Misc", enabled=funny),
    "Maid Outfit":                      LocationInfo("Buried near the light post on the last turn to TR3", "Misc", enabled=_and(funny, buried), rule=HasShovel()),

    **{f"Survive Day {i+1}":            LocationInfo("", "Tasks",
        enabled=lambda world, n=i: world.options.objective.value == VOTVGoal.SURVIVE and n == world.options.survive_day.value - 1 or n < world.options.survive_days_locations.value and (world.options.objective.value != VOTVGoal.SURVIVE or n < world.options.survive_day.value),
        rule=Has("Day", DayItemFieldResolver(i+1), options=[OptionFilter(DayAsItems, True)], filtered_resolution=True)
    ) for i in range(max_days)},
    **{f"Sell Level {j} Signal {i+1}":  LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < world.options.signal_locations.value,
        rule=Has("Progressive Processing Level", j, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True) & CanGetSignals(processing=j > 0)
    ) for j in range(4) for i in range(max_signal_locations)},
    **{f"Daily Task Done {i+1}":        LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < world.options.daily_task_locations.value,
        rule=Has("Day", DayItemFieldResolver(1), options=[OptionFilter(DayAsItems, True)], filtered_resolution=True) & CanGetSignals(processing=True),  # There's no daily taks on the first day. This assumes you start on day 1 (the whole world does tbh)
    ) for i in range(max_daily_tasks_locations)},
    **{f"Repair Server {i+1}":          LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.server_repair_locations.value) for i in range(max_server_repair_locations)},
    **{f"Repair Transformer {i+1}":     LocationInfo("", "Tasks", enabled=lambda world, n=i: n < world.options.transformer_repair_locations.value) for i in range(max_transformer_repair_locations)},
    **{f"Replace Fuse {i+1}":           LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < world.options.fuse_replacement_locations.value,
        rule=Has("Fuse", count=min(i+1, 10), options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True) & Has("Random Fuse Blowout", count=max(0, i-15))
    ) for i in range(max_fuse_replacement_locations)},
    **{f"Sell 24 Full Trash Bags {i+1}": LocationInfo("", "Tasks",
        enabled=lambda world, n=i: n < world.options.trash_bags_locations.value,
        rule=CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs")
    ) for i in range(max_trash_cleaning_locations)},
    **{f"Light the {dir} Candle":       LocationInfo("", "Tasks", enabled=candles, rule=Has("Lighter", options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True)) for dir in ('North', 'Northwest', 'West', 'Southwest', 'South', 'Southeast', 'East', 'Northeast')},

    "Repair the Oven":                  LocationInfo("", "Alpha Base", enabled=maintenance, region="Staff Room"),
    "Clean the Toilet":                 LocationInfo("", "Alpha Base", enabled=maintenance, region="Bathroom", rule=Has("Sponge", options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True)),
    "Clean the Sink":                   LocationInfo("", "Alpha Base", enabled=maintenance, region="Bathroom", rule=Has("Sponge", options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True)),
    "Clean the Shower":                 LocationInfo("", "Alpha Base", enabled=maintenance, region="Bathroom", rule=Has("Sponge", options=[OptionFilter(WorldItems, WorldItems.option_base, "ge")], filtered_resolution=True)),
    "Bake Cookies":                     LocationInfo("", "Alpha Base", enabled=cooking, region="Staff Room", rule=CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs")),
    "Bake Bread":                       LocationInfo("", "Alpha Base", enabled=cooking, region="Staff Room", rule=CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs")),
    "Bake a Pizza":                     LocationInfo("", "Alpha Base", enabled=cooking, region="Staff Room", rule=CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs")),

    **{f"Ball Joints Box {i+1}":        LocationInfo("In the gravel pile near Romeo", "Misc", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=_and(buried, world_item(WorldItems.option_hidden))), rule=HasShovel() & Has("Metal Detector")) for i in range(6)},
    **{f"TR{i+1} Limb Joints {j+1}":    LocationInfo("", f"TR{i+1}", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item(WorldItems.option_hidden)), region=f"TR{i+1} Room") for i in range(3) for j in range(2)},
    "Radioactive Capsule Blueprint":    LocationInfo("At the Green Hatch", "Green Hatch", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item())),
    "TR1 Gas Welder 1":                 LocationInfo("", "TR1", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item())),
    "TR1 Gas Welder 2":                 LocationInfo("", "TR1", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item())),
    "Hole Gas Welder":                  LocationInfo("", "The Hole", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item())),

    "Bunker Keycard":                   LocationInfo("Hookable from the slot at the back of the bunker", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item()), rule=Has("Bunker Keycard") & CanReachRegion("Bunker") | HasAny("Half Hook", "Hook")),
    "Kerfur-Omega Complete Manual":     LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item(WorldItems.option_hidden)), region="Bunker"),
    "Kerfur-Omega Documents Binder":    LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item()), region="Bunker"),

    "Pickaxe":                          LocationInfo("", "Lake", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item()), region="Lake"),
    "Omega AI Module":                  LocationInfo("", "Lake", complex=True, enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=world_item()), region="Lake", rule=HasAny("Half Hook", "Hook", "Hacksaw")),

    "Buried Radioactive Capsule":       LocationInfo("", "TR2", enabled=goal({VOTVGoal.KERFUR_OMEGA}, also=_and(buried, world_item(WorldItems.option_hidden))), rule=HasShovel()),
    "Crafted Radioactive Capsule":      LocationInfo("", "Misc", complex=True, enabled=_and(lambda world: bool(world.options.enable_crafted_capsule.value), goal({VOTVGoal.KERFUR_OMEGA}, also=world_item())), region="Cave", rule=HasAll("Hazmat Suit", "Gas Welder", "Radioactive Capsule Blueprint", "Pickaxe") & HasAny("Half Hook", "Hook")),

    "Basement Skull":                   LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=world_item(WorldItems.option_hidden)), region="Alpha Stairs"),
    "Buried Box Skull":                 LocationInfo("At 263.25/-7.25", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=_and(buried, world_item(WorldItems.option_extreme))), rule=HasShovel()),
    "Gravel Circle Skull":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=world_item(WorldItems.option_hidden))),
    "Radioactive Capsule Skull":        LocationInfo("", "TR2", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=world_item(WorldItems.option_hidden))),
    "Cave Entrance Skull":              LocationInfo("", "Cave", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=world_item())),
    "Stonehenge Skull":                 LocationInfo("", "Stonehenge", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=world_item()), region="Stonehenge"),
    "Rozital Ship Skull":               LocationInfo("", "Misc", enabled=goal({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=_and(lambda w: lifecrystal_signal_enabled(w), world_item(WorldItems.option_extreme))), rule=HasShovel() & Has("Lifecrystal Signal") & CanGetSignals(processing=True) & Has("Progressive Processing Level", 3, options=[OptionFilter(UpgradesAsItems, UpgradesAsItems.option_useful, "ge")], filtered_resolution=True)),

    "Fire Rune":                        LocationInfo("Explode a rock, violently", "Misc", complex=True, enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=world_item(WorldItems.option_extreme)), rule=Has("Half Hook", count=2) | Has("Hook")),
    "Earth Rune":                       LocationInfo("Bury a rock in the big log near TR2 and dig it up between 0:00 and 1:00", "Misc", complex=True, enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=_and(buried, time_sensitive, world_item(WorldItems.option_extreme))), rule=HasShovel()),
    "Water Rune":                       LocationInfo("Send a rock off the map in the river near the Lake and catch it on the other side", "Misc", complex=True, enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=world_item(WorldItems.option_extreme))),
    "Air Rune":                         LocationInfo("Send a rock to the top of the map with balloons", "Misc", complex=True, enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=world_item(WorldItems.option_extreme)), rule=Has("Balloon Pack (WIP)")),
    "Ritual Knife":                     LocationInfo("In the Lambert Ritual dimension, accessible in the Abandoned Shack at 3:33 AM", "Abandoned Shack", complex=True, enabled=goal({VOTVGoal.LAMBERT_PLUSH}, also=_and(time_sensitive, world_item(WorldItems.option_hidden))), region="Abandoned Shack"), # Maybe extreme?

    # All the argemia plushes are put at the "None" world item tier to be entirely controlled by their own option
    # "Shrimp Pack":                      LocationInfo("In the fridge", "Alpha Base", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), region="Staff Room"),  # Disabled for randomizing its key
    "Red Argemia Plush":                LocationInfo("In the hole near the estuary of the river in the top right", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb))),
    "Blue Argemia Plush":               LocationInfo("In the river between the first two bridges when walking towards the base", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb))),
    "Green Argemia Plush":              LocationInfo("At the top of the mountain in the bottom left, out of fence", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgb)), rule=CanReachRegion("Garage") & Has("Gas Can") | HasAny("Half Hook", "Hook", "Hiking Boots")),
    "Yellow Argemia Plush":             LocationInfo("Place a shrimp pack at each corner of the map and in the basement, then look up and away after midnight", "Misc", complex=True, enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), region="Alpha Stairs", rule=Has("Shrimp Pack", 16) & CanReachRegion("Staff Room") & CanReachRegion("Restricted Area")),
    "Cyan Argemia Plush":               LocationInfo("Put 12 shrimp packs in the emergency shower, and explode them", "Misc", complex=True, enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=argemia_plush(ArgemiaPlushes.option_rgbycm)), region="Signal Lab", rule=Has("Shrimp Pack", 16) & CanReachRegion("Staff Room")),  # 17, -1 since we assume the players have the fridge Shrimp Pack
    "Magenta Argemia Plush":            LocationInfo("At the Rozital Ship after the lifecrystal signal is downloaded", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, also=lambda w: lifecrystal_signal_enabled(w)), rule=Has("Lifecrystal Signal") & CanGetSignals(processing=False)),
    "Nuclear Pink Argemia Plush":       LocationInfo("Near the radio tower at 35.23/-37.24, invisible until bumped", "Misc", enabled=argemia_plush(ArgemiaPlushes.option_all)),
    "Nuclear Yellow Argemia Plush":     LocationInfo("At -634.14/181.37", "Misc", enabled=_and(buried, argemia_plush(ArgemiaPlushes.option_all)), rule=HasShovel() & Has("Metal Detector")),
    "Nuclear Orange Argemia Plush":     LocationInfo("Next to the barrier at 872.25/-793.0, high in the sky", "Misc", enabled=argemia_plush(ArgemiaPlushes.option_all), rule=HasAny("Half Hook", "Hook")),

    "Alpha Roof Tile":                  LocationInfo("Above the living quarters", "Alpha Base", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_hidden)), region="Alpha Roof"),
    "Alpha Bridge Tile":                LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_extreme))),
    "Xray Tile":                        LocationInfo("Above the nearby lightning rod", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_extreme)), rule=HasAny("Half Hook", "Hook")),
    "TR2 Tile":                         LocationInfo("At the base of a tree nearby, in the direction of the Radioactive Capsule", "TR2", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_extreme))),
    "Hole Tile":                        LocationInfo("Behind the rocks", "The Hole", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_hidden))),
    "CR3 Tile":                         LocationInfo("On the second-to-last floor", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_hidden))),
    "Sierra Tile":                      LocationInfo("On the right of the server room", "Misc", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_hidden))),
    "Stolas Church Tile":               LocationInfo("At the very top, in the empty window", "Village", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item(WorldItems.option_extreme)), rule=HasAny("Half Hook", "Hook")),
    "Green Cabinet Tile":               LocationInfo("", "Green Cabinet", enabled=goal({VOTVGoal.GREEN_CABINET}, also=world_item())),

    "Kerfur-Omega":                     LocationInfo("", "Alpha Base", enabled=goal({VOTVGoal.KERFUR_OMEGA}, final=True), rule=(
        HasFromList("Red Kerfur", "Blue Kerfur", "Pink Kerfur", count=2) & HasAllCounts({"Radioactive Capsule": 1, "Omega AI Module": 1, "Limb Joint": 4, "Ball Joint": 8, "Progressive Camera": 3, "Kerfur-Omega Complete Manual": 1})
        & HasAll(*(f"{x} Scrap Recipe" for x in ("Plastic", "Metal", "Glass", "Electronic")), options=[OptionFilter(ScrapRecipesAsItems, True)], filtered_resolution=True)
    )),
    "Hell Rock":                        LocationInfo("", "Stonehenge", enabled=goal({VOTVGoal.HELL_ROCK}, final=True), region="Stonehenge", rule=HasAllCounts({"Skull": 7})),
    "White Argemia Plush":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.WHITE_ARGEMIA_PLUSH}, final=True), rule=HasAllCounts({"Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Black Argemia Plush":              LocationInfo("", "Misc", enabled=goal({VOTVGoal.BLACK_ARGEMIA_PLUSH}, final=True), region="Stonehenge", rule=HasAllCounts({"Skull": 7, "Red Argemia Plush": 1, "Green Argemia Plush": 1, "Blue Argemia Plush": 1, "Yellow Argemia Plush": 1, "Cyan Argemia Plush": 1, "Magenta Argemia Plush": 1})),
    "Lambert Plush":                    LocationInfo("", "Abandoned Shack", enabled=goal({VOTVGoal.LAMBERT_PLUSH}, final=True), region="Abandoned Shack", rule=HasAllCounts({"Fire Rune": 1, "Earth Rune": 1, "Water Rune": 1, "Air Rune": 1, "Ritual Knife": 1})),
    "Open the Green Cabinet":           LocationInfo("", "Green Cabinet", enabled=goal({VOTVGoal.GREEN_CABINET}, final=True), rule=HasAllCounts({"Tile": 9})),
}
