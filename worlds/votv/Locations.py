# Look at init or Items.py for more information on imports
from typing import TYPE_CHECKING
import logging

from .Types import LocData, VOTVGoal
from .Constants import allowed_unlocks
from .data.item_data import shop_items
from .data.location_data import locations

if TYPE_CHECKING:
    from . import VOTVWorld

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "VOTVWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

def is_goal_enabled(world: "VOTVWorld", goal: VOTVGoal):
    return (world.options.objective == goal
        or goal == VOTVGoal.KERFUR_OMEGA and world.options.kerfur_omega_enabled.value
        or goal == VOTVGoal.HELL_ROCK and world.options.hell_rock_enabled.value
        or goal == VOTVGoal.LAMBERT_PLUSH and world.options.lambert_plush_enabled.value
        or goal == VOTVGoal.GREEN_CABINET and world.options.green_cabinet_enabled.value)

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "VOTVWorld", name: str) -> bool:
    if name.startswith("Purchase") and not world.options.shop_items.value:
        return False

    if name.endswith("Argemia Plush"):
        has_argemia_plush_objective = world.options.objective in (VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH)
        if name.startswith("Red") or name.startswith("Green") or name.startswith("Blue"):
            return world.options.argemia_plushes.value > 0 or has_argemia_plush_objective

        if name.startswith("Yellow") or name.startswith("Cyan") or name.startswith("Magenta"):
            return world.options.argemia_plushes.value > 1 or has_argemia_plush_objective

        if name.startswith("Nuclear"):
            return world.options.argemia_plushes.value > 2

    if name.startswith("Survive Day"):
        max_day = world.options.survive_day if world.options.objective == VOTVGoal.SURVIVE else world.options.survive_days_locations
        return int(name.split(" ")[-1]) <= max_day

    if name.startswith("Sell Level"):
        count = world.options.signal_locations
        return int(name.split(" ")[-1]) <= count

    if name.startswith("Daily Task Done"):
        count = world.options.daily_task_locations
        return int(name.split(" ")[-1]) <= count

    if name.startswith("Repair Server"):
        count = world.options.server_repair_locations
        return int(name.split(" ")[-1]) <= count

    if name.startswith("Repair Transformer"):
        count = world.options.transformer_repair_locations
        return int(name.split(" ")[-1]) <= count

    if name.startswith("Replace Fuse"):
        count = world.options.fuse_replacement_locations
        return int(name.split(" ")[-1]) <= count

    if "Full Trash Bags" in name:
        count = world.options.trash_bags_locations
        return int(name.split(" ")[-1]) <= count

    if name not in locations:
        return True
    location_info = locations[name]

    if len(location_info.goals) > 0:
        if location_info.is_final and world.options.objective not in location_info.goals:
            return False

        if not any(is_goal_enabled(world, goal) for goal in location_info.goals):
            return False

    if location_info.is_funny and not world.options.funny_setting.value:
        return False

    if (
        location_info.is_time_sensitive
        and not world.options.time_sensitive.value
        and world.options.objective not in location_info.goals
    ):
        return False

    if (
        location_info.is_buried
        and not world.options.buried_items.value
        and world.options.objective not in location_info.goals
    ):
        return False

    # I know it's weird to do tri-state like that, but it works
    if location_info.radioactive_capsule_craft_required == True and not world.options.require_mining.value:
        return False

    if location_info.radioactive_capsule_craft_required == False and world.options.require_mining.value:
        return False
    
    if location_info.maintenance_task and not world.options.maintenance_tasks.value:
        return False
    
    if location_info.cooking_task and not world.options.cooking_tasks.value:
        return False

    return True

votv_locations: dict[str, LocData] = {}

current_id = len(votv_locations) + 1
for item_name in shop_items.keys():
    item = shop_items[item_name]
    if not item.checkUnlock(allowed_unlocks):
        continue
    votv_locations[f"Purchase {item_name}"] = LocData(current_id, "World")
    current_id += 1

for name, info in locations.items():
    votv_locations[name] = LocData(current_id, "World")
    current_id += 1

# from .data.achievement_data import *
# for achievement in achievements:
#     votv_locations[achievement] = LocData(current_id, "World")
#     current_id += 1
# for advancement in advancements:
#     votv_locations[advancement] = LocData(current_id, "World")
#     current_id += 1

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations: dict[str, LocData] = {}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **votv_locations,
    **event_locations
}
