from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import MOTHERWorld



# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amoount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "MOTHERWorld"):
    player = world.player
    options = world.options

    # Chapter Access
    #IMPORTANT - add_rule is required to init the rule. otherwise add_rule should be fine
    #keys

    #MyHome
    add_rule(world.multiworld.get_entrance("MyHome -> MyHome (Basement)", player),
             lambda state: state.has("BasementKey", player))

    #Podunk
    add_rule(world.multiworld.get_entrance("Podunk -> Zoo", player),
             lambda state: state.has("Zoo Key", player))
    add_rule(world.multiworld.get_location("Zoo Key", player),
             lambda state: state.has_all(["Pippi", "Ninten"], player))
    add_rule(world.multiworld.get_location("Canary Melody", player),
             lambda state: state.has("CanaryChick", player))
    add_rule(world.multiworld.get_location("Franklin Badge", player),
             lambda state: state.has("Pippi", player))

    #add Spookane, Reindeer, and Snowman based on whether or not you want to
    #walk for five years and also probably die a lot
    do_trainpath_trek = bool(world.options.NoTrainTrainpath.value)
    trainpath_hard = ["Spookane", "Reindeer", "Snowman"]
    if not do_trainpath_trek:
        trainpath_hard = []

    #For every "World -> " entrance, set accordingly
    for entrance in world.multiworld.get_entrances(player):
        if not entrance.name.startswith("World"):
            continue

        dest_region = entrance.name.split(" -> ")[-1]
        #get to merrysville
        if not dest_region in ["Podunk"]:
            add_rule(entrance,
                lambda state: (state.has_all(["GGF's Diary", "Zoo Key"], player) and state.has_any(["Ninten", "Ana"], player)) or
                            state.has("Onyx Hook", player))
        #get to anywhere fucking else
        if not dest_region in ["Podunk",
                               "Magicant", "Merrysville"] + trainpath_hard:
            add_rule(entrance,
                lambda state: state.has_all(["Lloyd", "Pass", "Duncan Rocket"], player))

    #Magicant
    #needs telepathy
    add_rule(world.multiworld.get_entrance("Magicant -> Castle", player),
             lambda state: state.has_any(["Ninten", "Ana"], player))
    add_rule(world.multiworld.get_location("Magic Ribbon", player),
             lambda state: state.has("Ana", player))
    add_rule(world.multiworld.get_location("Magic Candy", player),
             lambda state: state.has("Lloyd", player))
    add_rule(world.multiworld.get_location("Big Bag", player),
             lambda state: state.has("Cash Card", player))

    #Merrysville
    add_rule(world.multiworld.get_entrance("Merrysville -> Duncan's Factory", player),
             lambda state: state.has("Pass", player))
    add_rule(world.multiworld.get_location("Recruit Lloyd", player),
             lambda state: state.has_any(["BottlRocket", "Lloyd's Bottle Rocket"], player))
    for i in range(4):
        add_rule(world.multiworld.get_location(f"Twinkle Scientist {i+1}", player),
                lambda state: state.has("Lloyd", player))

    #Reindeer
    add_rule(world.multiworld.get_location("Mouthwash Fill", player),
             lambda state: state.has("Dentures", player))
    add_rule(world.multiworld.get_location("Mouthwash Repeatable", player),
             lambda state: state.has("Dentures", player))

    #Spookane
    add_rule(world.multiworld.get_entrance("Spookane -> Rosemary Mansion", player),
             lambda state: state.has("Ghost Key", player))

    #Snowman
    add_rule(world.multiworld.get_location("Recruit Ana", player),
             lambda state: state.has("Hat", player))

    #Yucca Desert
    add_rule(world.multiworld.get_entrance("Yucca Desert -> Monkey Cave", player),
            lambda state: state.has("Ticket Stub", player, 10))

    #Ellay
    add_rule(world.multiworld.get_location("Recruit Teddy", player),
             lambda state: state.has_all(["Lloyd", "Ticket"], player))
    add_rule(world.multiworld.get_location("Island Scientist", player),
            lambda state: state.has("berry Tofu", player))
    add_rule(world.multiworld.get_location("Island Able", player),
            lambda state: state.has("berry Tofu", player))
    add_rule(world.multiworld.get_location("Island Baker", player),
            lambda state: state.has("berry Tofu", player))

    #Mt. Itoi
    add_rule(world.multiworld.get_entrance("Mt. Itoi -> Path To Giegue", player),
             lambda state: state.has("Maria's Love", player))
    add_rule(world.multiworld.get_location("Beat Giegue", player),
             lambda state: state.has("Maria's Love", player))
    add_rule(world.multiworld.get_location("EVE Melody", player),
            lambda state: state.has("Lloyd", player))

    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
