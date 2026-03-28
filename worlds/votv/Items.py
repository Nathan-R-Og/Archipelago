# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# When a list is described its described as a list of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, VOTVItem
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING
from .data.item_data import shop_items

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import VOTVWorld

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "VOTVWorld") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []

    #party_shuffle = party_shuffle_table[world.options.PartyShuffle.value]
    #starting_character = starting_character_table[world.options.StartingCharacter.value]

    #world.multiworld.push_precollected(create_item(world, "Cash Card"))
    #world.multiworld.push_precollected(create_item(world, starting_character))

    shuffle_blacklist = [
    #    "Cash Card",
        "Victory"
    ]
    #shuffle_blacklist.append(starting_character)

    victory = create_item(world, "Victory")
    Boss = world.multiworld.get_location("Survived Day 50", world.player)
    Boss.place_locked_item(victory)
    locked_locations = 1

    shuffle_pool = list(votv_items.keys())

    allowed_unlocks = []
    for item in shuffle_pool:
        if item in shuffle_blacklist:
            continue

        if item in shop_items.keys():
            itemd = shop_items[item]
            if not itemd.checkUnlock(allowed_unlocks):
                continue

        if item_table[item].count > 1:
            itempool += create_multiple_items(world, item, item_table[item].count, item_table[item].classification)
        else:
            result_item = create_item(world, item)
            itempool.append(result_item)

    #print(itempool)


    # Then junk items are made
    # Check out the create_junk_items function for more details
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - locked_locations)

    return itempool

# This is a generic function to create a singular item
def create_item(world: "VOTVWorld", name: str) -> Item:
    data = item_table[name]
    return VOTVItem(name, data.classification, data.ap_code, world.player)

# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "VOTVWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [VOTVItem(name, item_type, data.ap_code, world.player)]

    return itemlist

# Finally, where junk items are created
def create_junk_items(world: "VOTVWorld", count: int) -> List[Item]:
    trap_chance = world.options.TrapChance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    # This grabs all the junk items and trap items
    for name in item_table.keys():
        # Here we are getting all the junk item names and weights
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        # This is for traps if your randomization includes it
        # It also grabs the trap weights from the options page
        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "StoneOrigin":
                trap_list[name] = world.options.StoneOriginTrapWeight.value
            elif name == "PoisnNeedl":
                trap_list[name] = world.options.PoisnNeedleTrapWeight.value

    # Where all the magic happens of adding the junk and traps randomly
    # AP does all the weight management so we just need to worry about how many are created
    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well

votv_items = {
    "Day": ItemData(0, ItemClassification.progression, 50),
    "Victory": ItemData(1, ItemClassification.progression),
}
junk_items = {
}

junk_weights = {
}

#programatically create junk and items from the shop
current_id = len(votv_items)+len(junk_items)
for item_name in shop_items.keys():
    item = shop_items[item_name]

    if item.classification == ItemClassification.filler:
        junk_items[item_name] = ItemData(current_id, ItemClassification.filler)
        junk_weights[item_name] = 30
    else:
        votv_items[item_name] = ItemData(current_id, item.classification)
    current_id += 1

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **votv_items,
    **junk_items,
}

