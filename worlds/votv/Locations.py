# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import VOTVWorld

# This is technique in programming to make things more readable for booleans
# A boolean is true or false
def did_include_extra_locations(world: "VOTVWorld") -> bool:
    return bool(world.options.ExtraLocations)

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "VOTVWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        if not did_include_extra_locations(world) and name in extra_locations:
            continue

        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items()}

    return names

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "VOTVWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True

votv_locations = {}

current_id = len(votv_locations)
max_days = 50
last_day_report = True
for day in range(max_days):
    votv_locations[f"Survived Day {day+1}"] = LocData(current_id, "World")
    current_id += 1
    if day == 0:
        continue
    if day+1 < max_days or last_day_report:
        votv_locations[f"Day {day+1} Report"] = LocData(current_id, "World")
        current_id += 1

allowed_unlocks = []
from .data.item_data import shop_items
for item_name in shop_items.keys():
    item = shop_items[item_name]
    if not item.checkUnlock(allowed_unlocks):
        continue
    votv_locations[f"Purchase {item_name}"] = LocData(current_id, "World")
    current_id += 1

# from .data.achievement_data import *
# for achievement in achievements:
#     votv_locations[achievement] = LocData(current_id, "World")
#     current_id += 1
# for advancement in advancements:
#     votv_locations[advancement] = LocData(current_id, "World")
#     current_id += 1

extra_locations = {
    #"ml7's house": LocData(187, "Sibiu"),
}

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **votv_locations,
    **extra_locations,
    **event_locations
}