from typing import TYPE_CHECKING
from rule_builder.rules import Has

from .Locations import is_valid_location, location_table
from .data.location_data import locations

if TYPE_CHECKING:
    from . import VOTVWorld

def set_rules(world: "VOTVWorld"):
    player = world.player

    for name in location_table:
        if not is_valid_location(world, name):
            continue

        if name not in locations:
            continue
        location_info = locations[name]
        if location_info.rule is None:
            continue

        world.set_rule(world.multiworld.get_location(name, player), location_info.rule)

    # Victory condition rule!
    world.set_completion_rule(Has("Victory"))
