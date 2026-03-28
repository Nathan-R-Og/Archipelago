from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import VOTVWorld

def set_rules(world: "VOTVWorld"):
    player = world.player
    options = world.options
    max_days = 50
    for i in range(max_days+1):
        if i == 0:
            continue
        print(f"Survived Day {i}")
        print(i)
        add_rule(world.multiworld.get_location(f"Survived Day {i}", player),
                lambda state: state.has("Day", player, i))
        if i < 1 or i >= max_days:
            continue
        print(f"Day {i+1} Report")
        print(i)
        add_rule(world.multiworld.get_location(f"Day {i+1} Report", player),
                lambda state: state.has("Day", player, i))

    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
