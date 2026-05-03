# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# When a list is described its described as a list of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
from enum import IntEnum
import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification
from typing import TYPE_CHECKING, Sequence

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, VOTVGoal, VOTVItem
from .Locations import get_total_locations, is_goal_enabled
from .Constants import allowed_unlocks
from .data.item_data import ExtraClassification, shop_items, extra_items, goal_items

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import VOTVWorld

class ItemValidity(IntEnum):
    INVALID = 0
    VALID = 1
    PROGRESSION = 2

def is_valid_item(world: "VOTVWorld", name: str, classsfication: int) -> ItemClassification | None:
    if name == "Day" and not world.options.day_as_items.value:
        return None
    
    if name.endswith("Argemia Plush"):
        has_argemia_plush_objective = world.options.objective in (VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH)
        if not has_argemia_plush_objective:
            if name.startswith("Red") or name.startswith("Green") or name.startswith("Blue") and world.options.argemia_plushes.value == 0:
                return None

            if name.startswith("Yellow") or name.startswith("Cyan") or name.startswith("Magenta") and world.options.argemia_plushes.value <= 1:
                return None
        
        if name.startswith("Nuclear") and world.options.argemia_plushes.value <= 2:
            return None
        
    if name.endswith("Recipe") and not world.options.scrap_recipes_as_items:
        return None

    if name in shop_items:
        if not world.options.shop_items.value:
            return None

        itemd = shop_items[name]
        if not itemd.checkUnlock(allowed_unlocks):
            return None
    
    itemd = None
    if name in goal_items:
        itemd = goal_items[name]
        if world.options.objective not in itemd.goals:
            if not any(is_goal_enabled(world, goal) for goal in itemd.goals):
                return None
            
            itemd = itemd.alternate_item
        else:
            return ItemClassification.progression

    if name in extra_items:
        itemd = extra_items[name]

    if itemd:
        if classsfication & ExtraClassification.buried and not world.options.buried_items.value:
            return None

        if classsfication & ExtraClassification.time_sensitive and not world.options.time_sensitive.value:
            return None

        if classsfication & ExtraClassification.funny and not world.options.funny_setting.value:
            return None

    return ItemClassification(classsfication & 0b11111)

# If you're curious about the -> list[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "VOTVWorld") -> list[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    item_pool: list[Item] = []

    #party_shuffle = party_shuffle_table[world.options.PartyShuffle.value]
    #starting_character = starting_character_table[world.options.StartingCharacter.value]

    #world.multiworld.push_precollected(create_item(world, "Cash Card"))
    #world.multiworld.push_precollected(create_item(world, starting_character))

    shuffle_blacklist = [
        "Victory"
    ]
    #shuffle_blacklist.append(starting_character)

    victory = create_items(world, "Victory")[0]
    location_name = ""
    match world.options.objective:
        case VOTVGoal.KERFUR_OMEGA:
            location_name = "Kerfur-Omega"
        case VOTVGoal.HELL_ROCK:
            location_name = "Hell Rock"
        case VOTVGoal.WHITE_ARGEMIA_PLUSH:
            location_name = "White Argemia Plush"
        case VOTVGoal.BLACK_ARGEMIA_PLUSH:
            location_name = "Black Argemia Plush"
        case VOTVGoal.LAMBERT_PLUSH:
            location_name = "Lambert Plush"
        case VOTVGoal.GREEN_CABINET:
            location_name = "Green Cabinet Open"
        case VOTVGoal.SURVIVE:
            location_name = f"Survive Day {world.options.survive_day.value}"

    Boss = world.multiworld.get_location(location_name, world.player)
    Boss.place_locked_item(victory)
    locked_locations = 1

    shuffle_pool = list(item_table.keys())
    for name in shuffle_pool:
        if name in shuffle_blacklist:
            continue

        items = create_items(world, name)
        useful_or_progression_items = tuple(x for x in items if x.classification & ItemClassification.progression or x.classification & ItemClassification.useful)
        item_pool += useful_or_progression_items

    # Then junk items are made
    # Check out the create_junk_items function for more details
    item_pool += create_junk_items(world, get_total_locations(world) - len(item_pool) - locked_locations)

    return item_pool

def create_items(world: "VOTVWorld", name: str) -> list[Item]:
    item = item_table[name]
    result: list[Item] = []
    for classification, amount in item.classification.items():
        classification = is_valid_item(world, name, classification)
        if classification is None:
            continue
        result += (VOTVItem(name, classification, item.ap_code, world.player) for _ in range(amount))

    return result

# Finally, where junk items are created
def create_junk_items(world: "VOTVWorld", count: int) -> list[Item]:
    trap_chance = world.options.trap_chance.value
    junk_pool: list[Item] = []
    junk_list: list[str] = []
    trap_list: list[str] = []

    # This grabs all the junk items and trap items
    for name, item in item_table.items():
        if name == "Bonus Points":  # Special filler item used when there's not enough items
            continue

        for classification, amount in item.classification.items():
            classification = is_valid_item(world, name, classification)
            if classification is None:
                continue

            if classification == ItemClassification.filler:
                junk_list += (name for _ in range(amount))
            elif classification == ItemClassification.trap:
                trap_list += (name for _ in range(amount))

    # Where all the magic happens of adding the junk and traps randomly
    # AP does all the weight management so we just need to worry about how many are created
    for _ in range(count):
        current_list = junk_list
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            current_list = trap_list

        if len(current_list) == 0:
            junk_pool.append(world.create_item("Bonus Points"))
            continue

        name = world.random.choice(current_list)
        current_list.remove(name)
        junk_pool.append(world.create_item(name))

    return junk_pool

# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well
votv_items: dict[str, ItemData] = {
    "Victory": ItemData(1, {ItemClassification.progression: 1}),
    "Day": ItemData(2, {ItemClassification.progression: 50}),
}

# programatically create junk and items from the shop
current_id = len(votv_items) + 1
for name, item in shop_items.items():
    votv_items[name] = ItemData(current_id, {item.classification: 1})
    current_id += 1

for name, item in extra_items.items():
    votv_items[name] = ItemData(current_id, item.classification)
    current_id += 1

for name, item in goal_items.items():
    # If their goal is selected, the classification will be overriden with progression
    votv_items[name] = ItemData(current_id, item.alternate_item.classification)
    current_id += 1

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **votv_items,
    "Victory": ItemData(None, {ItemClassification.progression: 1})
}
