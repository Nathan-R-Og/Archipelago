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
from .Types import ItemData, MOTHERItem,\
    starting_character_table, party_shuffle_table
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import MOTHERWorld

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "MOTHERWorld") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []
    locked_locations = 0

    # This is a good place to grab anything you need from options
    party_shuffle = party_shuffle_table[world.options.PartyShuffle.value]

    starting_character = starting_character_table[world.options.StartingCharacter.value]

    #if party shuffle doesnt shuffle ninten, lock 'em
    if party_shuffle != "All":
        starting_character = "Ninten"

    print(party_shuffle)
    print(starting_character)

    # This creates your win item and then places it at the "location" where you win
    victory = create_item(world, "Victory")
    Boss = world.multiworld.get_location("Beat Giegue", world.player)
    Boss.place_locked_item(victory)
    locked_locations += 1

    world.multiworld.push_precollected(create_item(world, "Cash Card"))
    world.multiworld.push_precollected(create_item(world, starting_character))

    shuffle_blacklist = [
        "Victory",
        "Cash Card",
    ]
    shuffle_blacklist.append(starting_character)

    shuffle_pool = list(mother_items.keys())
    shuffle_pool += list(event_items.keys())
    shuffle_pool += list(party_items.keys())


    for item in shuffle_pool:
        if item in shuffle_blacklist:
            continue
        if item_table[item].count > 1:
            itempool += create_multiple_items(world, item, item_table[item].count, item_table[item].classification)
        else:
            result_item = create_item(world, item)
            itempool.append(result_item)

    print(itempool)


    # Then junk items are made
    # Check out the create_junk_items function for more details
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 1)

    return itempool

# This is a generic function to create a singular item
def create_item(world: "MOTHERWorld", name: str) -> Item:
    data = item_table[name]
    return MOTHERItem(name, data.classification, data.ap_code, world.player)

# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "MOTHERWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [MOTHERItem(name, item_type, data.ap_code, world.player)]

    return itemlist

# Finally, where junk items are created
def create_junk_items(world: "MOTHERWorld", count: int) -> List[Item]:
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

mother_items = {
# Progression items

#ITEMS EXPLICITLY REQUIRED TO REACH THE END
    #Allows entry to Merrysville
    "GGF's Diary": ItemData(19, ItemClassification.progression),
    #No checks but. yeah
    "Onyx Hook": ItemData(89, ItemClassification.progression),
    #Allows entry to Duncan
    "Pass": ItemData(2, ItemClassification.progression),
#not required but gets more checks
    #Allows entry to MyHome (Basement)
    "BasementKey": ItemData(5, ItemClassification.progression),
    #Allows entry to Zoo
    "Zoo Key": ItemData(18, ItemClassification.progression),
    #Check for Lloyd
    "Lloyd's Bottle Rocket": ItemData(6, ItemClassification.progression),
    #Check for Ana
    "Hat": ItemData(15, ItemClassification.progression),
    #Check for Teddy
    "Ticket": ItemData(16, ItemClassification.progression, 2),
    #Check for Tank Access
    "Ticket Stub": ItemData(17, ItemClassification.progression, 10),
    #Allows entry to Rosemary Mansion
    "Ghost Key": ItemData(20, ItemClassification.progression),
    #Gets Canary Melody
    "CanaryChick": ItemData(21, ItemClassification.progression),
    #Gets Mouthwash
    "Dentures": ItemData(24, ItemClassification.progression),


# Useful items
    "Cash Card": ItemData(23, ItemClassification.progression),

#game items
    #(7) are the global burger/drug vendors
    "LifeUpCream": ItemData(30, ItemClassification.useful, 11+(7)),

    "SportsDrink": ItemData(34, ItemClassification.useful, 4),
    "Rope": ItemData(37, ItemClassification.useful, 8),
    "MagicRibbon": ItemData(38, ItemClassification.useful),
    "Magic Candy": ItemData(39, ItemClassification.useful),
    "Magic Herb": ItemData(41, ItemClassification.useful, 12),
    "Repel Ring": ItemData(48, ItemClassification.useful, 2),
    "Red Weed": ItemData(53, ItemClassification.useful),
    "Bullhorn": ItemData(54, ItemClassification.useful),
    "Flashdark": ItemData(55, ItemClassification.useful),
    "PSI Stone": ItemData(56, ItemClassification.useful, 7),
    "FightCapsul": ItemData(58, ItemClassification.useful, 2),
    "Super Bomb": ItemData(63, ItemClassification.useful),
    "StkyMachine": ItemData(64, ItemClassification.useful),
    "QuickCapsul": ItemData(65, ItemClassification.useful, 3),
    "PhysicalCap": ItemData(67, ItemClassification.useful, 2),
    "BottlRocket": ItemData(68, ItemClassification.progression, 4+8),
    "Bomb": ItemData(71, ItemClassification.useful, 6),
    "Wisdom Caps": ItemData(72, ItemClassification.useful),
    "ForceCapsul": ItemData(73, ItemClassification.useful),
    "Super Spray": ItemData(74, ItemClassification.useful),
    "Mouthwash": ItemData(75, ItemClassification.useful, 3),
    "Laser Beam": ItemData(77, ItemClassification.useful),
    "Plasma Beam": ItemData(78, ItemClassification.useful),
    "Flea Bag": ItemData(79, ItemClassification.useful),

#equipment
##weapons
    "Plastic Bat": ItemData(26, ItemClassification.useful, 4),
    "Slingshot": ItemData(35, ItemClassification.useful, 2+3),
    "FranklnBdge": ItemData(36, ItemClassification.useful, 2),
    "Peace Coin": ItemData(42, ItemClassification.useful, 5),
    "ProtectCoin": ItemData(43, ItemClassification.useful, 5),
    "Magic Coin": ItemData(44, ItemClassification.useful, 5),
    "Brass Ring": ItemData(45, ItemClassification.useful, 5),
    "Silver Ring": ItemData(46, ItemClassification.useful, 5),
    "Gold Ring": ItemData(47, ItemClassification.useful, 5),
    "H2o Pendant": ItemData(49, ItemClassification.useful, 5),
    "FirePendant": ItemData(50, ItemClassification.useful, 5),
    "EarthPendnt": ItemData(51, ItemClassification.useful, 5),
    "Sea Pendant": ItemData(52, ItemClassification.useful),
    "Boomerang": ItemData(57, ItemClassification.useful, 3+2),
    "Sword": ItemData(61, ItemClassification.useful),
    "ButterKnife": ItemData(66, ItemClassification.useful),
    "AluminumBat": ItemData(69, ItemClassification.useful, 2),
    "Stun Gun": ItemData(70, ItemClassification.useful),
    "Frying Pan": ItemData(76, ItemClassification.useful),
    "NonstickPan": ItemData(80, ItemClassification.useful),
    "Air Gun": ItemData(81, ItemClassification.useful),
    "Surv.Knife": ItemData(82, ItemClassification.useful),
    "Katana": ItemData(85, ItemClassification.useful),
    "IronSkillet": ItemData(86, ItemClassification.useful),
    "Hank's Bat": ItemData(87, ItemClassification.useful),

#borderline filler
    "Ocarina": ItemData(40, ItemClassification.useful),
    "Ruler": ItemData(59, ItemClassification.useful, 2),
    "berry Tofu": ItemData(60, ItemClassification.progression, 3),
    "Last Weapon": ItemData(62, ItemClassification.useful),
    "Phone Card": ItemData(88, ItemClassification.useful),
    "Swear Words": ItemData(83, ItemClassification.useful),
    "WordsO'Love": ItemData(84, ItemClassification.useful),


    #Null: 10


# Victory is added here since in this organization it needs to be in the default item pool
    "Victory": ItemData(10, ItemClassification.progression)
}

event_items = {
    #Allows entry to Giegue
    "Maria's Love": ItemData(4, ItemClassification.progression),

    #Allows entry past Merrysville
    "Duncan Rocket": ItemData(3, ItemClassification.progression),
}

party_items = {
    "Ninten": ItemData(22, ItemClassification.progression),
    "Ana": ItemData(7, ItemClassification.progression),
    "Teddy": ItemData(8, ItemClassification.progression),
    "Pippi": ItemData(9, ItemClassification.progression),
    "Lloyd": ItemData(1, ItemClassification.progression | ItemClassification.useful),
}

# In the way that I made items, I added a way to specify how many of an item should exist
# That's why junk has a 0 since how many are created is in the create_junk_items
# There is a better way of doing this but this is my jank
junk_items = {
    # Junk
    "Bread": ItemData(27, ItemClassification.filler, 10),
    "OrangeJuice": ItemData(25, ItemClassification.filler, 6+(7)),
    "Antidote": ItemData(28, ItemClassification.filler, 7+(7)),
    "AsthmaSpray": ItemData(29, ItemClassification.filler, (7)),
    "Insecticide": ItemData(31, ItemClassification.filler, (7)),
    "FrenchFries": ItemData(32, ItemClassification.filler, (7)),
    "Hamburger": ItemData(33, ItemClassification.filler, (7)),

    # Traps
    #causes Petrification
    "StoneOrigin": ItemData(13, ItemClassification.trap, 0),
    #inflicts Poison
    "PoisnNeedle": ItemData(14, ItemClassification.trap, 0),
}

# Junk weights is just how often an item will be chosen when junk is being made
# Bigger item = more likely to show up
junk_weights = {
    "Bread": 30,
    "OrangeJuice": 30,
    "Antidote": 20,
    "AsthmaSpray": 20,
    "Insecticide": 20,
    "FrenchFries": 20,
    "Hamburger": 10,
}

psi_items = {
    #Gets Teleport / Access to MagiCastle
    "Telepathy": ItemData(91, ItemClassification.progression),
    #Access to literally anything
    "Teleport": ItemData(90, ItemClassification.progression),

}

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **mother_items,
    **event_items,
    **party_items,
    **junk_items,
}

