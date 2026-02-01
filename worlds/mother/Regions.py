from BaseClasses import Region
from .Types import MOTHERLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MOTHERWorld

# This is where you will create your imaginary game world
# IE: connect rooms and areas together
# This is NOT where you'll add requirements for how to get to certain locations thats in Rules.py
# This is also long and tediouos
def create_regions(world: "MOTHERWorld"):
    # The functions that are being used here will be located at the bottom to view
    # The important part is that if its not a dead end and connects to another place then name it
    # Otherwise you can just create the connection. Not that naming it is bad

    # You can technically name your connections whatever you want as well
    # You'll use those connection names in Rules.py
    r_world = create_region(world, "World")
    myhome = create_region_and_connect(world, "MyHome", "World -> MyHome", r_world)
    myhome_basement = create_region_and_connect(world, "MyHome (Basement)", "MyHome -> MyHome (Basement)", myhome)
    podunk = create_region_and_connect(world, "Podunk", "World -> Podunk", r_world)
    merrysville = create_region_and_connect(world, "Merrysville", "World -> Merrysville", r_world)
    magicant = create_region_and_connect(world, "Magicant", "World -> Magicant", r_world)
    castle = create_region_and_connect(world, "Castle", "Magicant -> Castle", magicant)
    zoo = create_region_and_connect(world, "Zoo", "Podunk -> Zoo", podunk)
    mt_itoi = create_region_and_connect(world, "Mt. Itoi", "World -> Mt. Itoi", r_world)
    path_to_giegue = create_region_and_connect(world, "Path To Giegue", "Mt. Itoi -> Path To Giegue", mt_itoi)
    duncans_factory = create_region_and_connect(world, "Duncan's Factory", "Merrysville -> Duncan's Factory", merrysville)

    snowman = create_region_and_connect(world, "Snowman", "World -> Snowman", r_world)
    reindeer = create_region_and_connect(world, "Reindeer", "World -> Reindeer", r_world)
    spookane = create_region_and_connect(world, "Spookane", "World -> Spookane", r_world)
    rosemary_mansion = create_region_and_connect(world, "Rosemary Mansion", "Spookane -> Rosemary Mansion", spookane)
    ellay = create_region_and_connect(world, "Ellay", "World -> Ellay", r_world)
    island = create_region_and_connect(world, "Island", "Ellay -> Island", ellay)
    yucca_desert = create_region_and_connect(world, "Yucca Desert", "World -> Yucca Desert", r_world)
    monkey_cave = create_region_and_connect(world, "Monkey Cave", "Yucca Desert -> Monkey Cave", yucca_desert)
    youngtown = create_region_and_connect(world, "Youngtown", "World -> Youngtown", r_world)

    #romania = create_region_and_connect(world, "Romania", "Menu -> Romania", menu)
    #sewer = create_region_and_connect(world, "The Sewer", "Menu -> The Sewer", menu)

    # ---------------------------------- Green Hill Zone ----------------------------------
    #greenhillzone1 = create_region_and_connect(world, "Green Hill Zone - Act 1", "Green Hill Zone -> Green Hill Zone - Act 1", greenhillzone)
    #greenhillzone2 = create_region_and_connect(world, "Green Hill Zone - Act 2", "Green Hill Zone - Act 1 -> Green Hill Zone - Act 2", greenhillzone1)
    #create_region_and_connect(world, "Green Hill Zone - Act 3", "Green Hill Zone - Act 2 -> Green Hill Zone - Act 3", greenhillzone2)

    # ---------------------------------- Romania ------------------------------------------
    #bucharest = create_region_and_connect(world, "Bucharest", "Romania -> Bucharest", romania)
    #sibiu = create_region_and_connect(world, "Sibiu", "Romania -> Sibiu", romania)
    #brașov = create_region_and_connect(world, "Brașov", "Romania -> Brașov", romania)
    #bucharest.connect(sibiu, "Bucharest -> Sibiu")
    #sibiu.connect(brașov, "Sibiu -> Brașov")
    #brașov.connect(bucharest, "Brașov, Bucharest")

    # ---------------------------------- The Sewer ----------------------------------------
    #create_region_and_connect(world, "Big Hole in the Floor", "The Sewer -> Big Hole in the Floor", sewer)

def create_region(world: "MOTHERWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = MOTHERLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)

    world.multiworld.regions.append(reg)
    return reg

# This runs the create region function while also connecting to another region
# Just simplifies process since you woill be connecting a lot of regions
def create_region_and_connect(world: "MOTHERWorld",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg