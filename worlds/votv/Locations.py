from typing import TYPE_CHECKING

from .Types import LocData
from .Constants import allowed_unlocks
from .data.shop_item_data import shop_items
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

def get_location_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}
    for name, location in locations.items():
        if location.group not in groups:
            groups[location.group] = set()
        groups[location.group].add(name)
    return groups

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "VOTVWorld", name: str) -> bool:
    if name.startswith("Purchase"):  # and not world.options.shop_items.value
        return False

    if name not in locations:
        return True
    location_info = locations[name]

    if not location_info.enabled(world):
        return False

    return True

votv_locations: dict[str, LocData] = {}

current_id = len(votv_locations) + 1
for item_name in shop_items.keys():
    item = shop_items[item_name]
    if not item.checkUnlock(allowed_unlocks):
        continue
    votv_locations[f"Purchase {item_name}"] = LocData(current_id, "Signal Lab")
    current_id += 1

for name, info in locations.items():
    votv_locations[name] = LocData(current_id, info.region)
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
