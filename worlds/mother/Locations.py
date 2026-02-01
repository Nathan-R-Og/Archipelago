# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import MOTHERWorld

# This is technique in programming to make things more readable for booleans
# A boolean is true or false
def did_include_extra_locations(world: "MOTHERWorld") -> bool:
    return bool(world.options.ExtraLocations)

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "MOTHERWorld") -> int:
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
def is_valid_location(world: "MOTHERWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
mother_locations = {
    # You can take a peak at Types.py for more information but,
    # LocData is code, region in this instance
    # Regions will be explained more in Regions.py
    # But just know that it's mostly about organization
    # Place locations together based on where they are in the game and what is needed to get there

    #OBJ_MYHOME_MINNIE_INVASION - 0x3c - OrangeJuice
    #OBJ_MYHOME_MIMMIE - 0x3c - OrangeJuice
    "Sister OJ": LocData(0, "MyHome"),

    "Doll Melody": LocData(1, "MyHome"),

    #OBJ_MYHOME_PRESENT1 - Plastic Bat
    "Basement Present 1": LocData(2, "MyHome (Basement)"),
    #OBJ_MYHOME_PRESENT2 - Bread
    "Basement Present 2": LocData(3, "MyHome (Basement)"),
    #OBJ_MYHOME_PRESENT3 - GGF's Diary
    "Basement Present 3": LocData(4, "MyHome (Basement)"),

    #OBJ_MYHOME_DOG - 0x55 - BasementKey
    "BasementKey": LocData(5, "MyHome"),
    #OBJ_PODUNK_ABBOTT - 0x56 - Zoo Key
    "Zoo Key": LocData(6, "Podunk"),

    #OBJ_MERRYSVILLE_DRUGSVENDOR
	#Antidote
	#AsthmaSpray
	#LifeUpCream
	#Insecticide
    "Drugs Vendor 1": LocData(7, "World"),
    "Drugs Vendor 2": LocData(8, "World"),
    "Drugs Vendor 3": LocData(9, "World"),
    "Drugs Vendor 4": LocData(10, "World"),

    #OBJ_PODUNK_BURGERWAITRESS
	#OrangeJuice
	#FrenchFries
	#Hamburger
	#Null
    "Burger 1": LocData(11, "World"),
    "Burger 2": LocData(12, "World"),
    "Burger 3": LocData(13, "World"),
    "Burger 4": LocData(14, "World"),

    #OBJ_PODUNK_FOODSVENDOR
	#OrangeJuice
	#Bread
	#SportsDrink
	#Null
    "Podunk Foods 1": LocData(15, "Podunk"),
    "Podunk Foods 2": LocData(16, "Podunk"),
    "Podunk Foods 3": LocData(17, "Podunk"),
    "Podunk Foods 4": LocData(18, "Podunk"),

    #OBJ_PODUNK_SPORTSVENDOR
	#Plastic Bat
	#Slingshot
	#Wooden Bat
	#Null
    "Podunk Sports 1": LocData(19, "Podunk"),
    "Podunk Sports 2": LocData(20, "Podunk"),
    "Podunk Sports 3": LocData(21, "Podunk"),
    "Podunk Sports 4": LocData(22, "Podunk"),


    #OBJ_PODUNK_PIPPI - 0x68 - FranklnBdge
    #OBJ_GRAVEYARD_PIPPI - 0x68 - FranklnBdge
    "Franklin Badge": LocData(23, "Podunk"),

    #OBJ_PODUNK_PETVENDOR - 0x5f - CanaryChick
    "Podunk Canary": LocData(24, "Podunk"),

    "Canary Melody": LocData(25, "Podunk"),

    #OBJ_ZOO_PRESENT1 - Antidote
    "Zoo Present 1": LocData(26, "Zoo"),
    #OBJ_ZOO_PRESENT2 - Rope
    "Zoo Present 2": LocData(27, "Zoo"),
    #OBJ_ZOO_PRESENT3 - Bread
    "Zoo Present 3": LocData(28, "Zoo"),
    #OBJ_ZOO_PRESENT4 - LifeUpCream
    "Zoo Present 4": LocData(29, "Zoo"),

    "Monkey Melody": LocData(30, "Zoo"),

    #OBJ_MAGICANT_ANACAT - 0x4b - MagicRibbon
    "Magic Ribbon": LocData(31, "Magicant"),
    #OBJ_MAGICANT_LLOYDCAT - 0x4c - Magic Candy
    "Magic Candy": LocData(32, "Magicant"),
    #OBJ_MAGICANT_OCARINAMAN - 0x66 - Ocarina
    "Ocarina": LocData(33, "Magicant"),
    #OBJ_MAGICANT_BIGBAGGUY - 0x6e - Cash Card
    "Big Bag": LocData(34, "Magicant"),

    #OBJ_MAGICANT_COINVENDOR
	#Magic Herb
	#Peace Coin
	#ProtectCoin
	#Magic Coin
    "Coin Shop 1": LocData(35, "Magicant"),
    "Coin Shop 2": LocData(36, "Magicant"),
    "Coin Shop 3": LocData(37, "Magicant"),
    "Coin Shop 4": LocData(38, "Magicant"),

    #OBJ_MAGICANT_RINGVENDOR
	#Magic Herb
	#Brass Ring
	#Silver Ring
	#Gold Ring
    "Ring Shop 1": LocData(39, "Magicant"),
    "Ring Shop 2": LocData(40, "Magicant"),
    "Ring Shop 3": LocData(41, "Magicant"),
    "Ring Shop 4": LocData(42, "Magicant"),

    #OBJ_MAGICANT_PENDANTVENDOR
	#Repel Ring
	#H2o Pendant
	#FirePendant
	#EarthPendnt
    "Pendant Shop 1": LocData(43, "Magicant"),
    "Pendant Shop 2": LocData(44, "Magicant"),
    "Pendant Shop 3": LocData(45, "Magicant"),
    "Pendant Shop 4": LocData(46, "Magicant"),

    #OBJ_MAGICANT_REDWEED - 0x6f - Red Weed
    "Red Weed 1": LocData(47, "Magicant"),
    #"Red Weed 2": LocData(48, "Magicant"), #Is Subrd
    #"Red Weed 3": LocData(49, "Magicant"), #Is Subrd
    #OBJ_MAGICANT_FOUNTAIN - 0x3e - Magic Herb
    "Red Weed Convert": LocData(50, "Magicant"),


    #OBJ_MAGICANT_CASTLEPRESENT1 - Bullhorn
    "Castle Present 1": LocData(51, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT2 - Antidote
    "Castle Present 2": LocData(52, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT3 - Magic Herb
    "Castle Present 3": LocData(53, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT4 - Null
    "Castle Present 4": LocData(54, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT5 - Flashdark
    "Castle Present 5": LocData(55, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT6 - Antidote
    "Castle Present 6": LocData(56, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT7 - Magic Herb
    "Castle Present 7": LocData(57, "Castle"),
    #OBJ_MAGICANT_CASTLEPRESENT8 - Boomerang
    ##OBJ_MAGICANT_CASTLEPRESENT9 - PSI Stone
    ##OBJ_MAGICANT_CASTLEPRESENT10 - FightCapsul
    ##OBJ_MAGICANT_CASTLEPRESENT11 - Rope
    ##OBJ_MAGICANT_CASTLEPRESENT12 - Ruler
    ##OBJ_MAGICANT_CASTLEPRESENT13 - berry Tofu
    "Castle MultiPresent": LocData(58, "Castle"),

    "Maria's Love": LocData(59, "Castle"), #Doesnt give item in vanilla

    #OBJ_MAGICANT_DUNGEONPRESENT1 - Magic Herb
    "Dungeon Present 1": LocData(60, "Magicant"),
    #OBJ_MAGICANT_DUNGEONPRESENT2 - Sword
    "Dungeon Present 2": LocData(61, "Magicant"),
    #OBJ_MAGICANT_DUNGEONPRESENT3 - PSI Stone
    "Dungeon Present 3": LocData(62, "Magicant"),
    #OBJ_MAGICANT_DUNGEONPRESENT4 - Magic Herb
    "Dungeon Present 4": LocData(63, "Magicant"),
    #OBJ_MAGICANT_DUNGEONPRESENT5 - Onyx Hook
    "Onyx Hook": LocData(64, "Magicant"),

    "Dragon Melody": LocData(65, "Magicant"),

    #OBJ_TWINKLE_PRESENT1 - Slingshot
    "Twinkle Present 1": LocData(66, "Merrysville"),
    #OBJ_TWINKLE_PRESENT2 - Plastic Bat
    "Twinkle Present 2": LocData(67, "Merrysville"),

    #OBJ_TWINKLE_SCIENTIST
	#Last Weapon
	#Super Bomb
	#StkyMachine
	#166
    "Twinkle Scientist 1": LocData(68, "Merrysville"),
    "Twinkle Scientist 2": LocData(69, "Merrysville"),
    "Twinkle Scientist 3": LocData(70, "Merrysville"),
    "Twinkle Scientist 4": LocData(71, "Merrysville"),


    #OBJ_MERRYSVILLE_QUESTIONNAIRE - 0x2 - Phone Card
    "Phone Card": LocData(73, "Merrysville"),

    #OBJ_SWEETFACTORY_PRESENT1 - LifeUpCream
    "Sweet's Present 1": LocData(74, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT2 - QuickCapsul
    "Sweet's Present 2": LocData(75, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT3 - Plastic Bat
    "Sweet's Present 3": LocData(76, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT4 - Magic Herb
    "Sweet's Present 4": LocData(77, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT5 - FightCapsul
    "Sweet's Present 5": LocData(78, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT6 - Magic Herb
    "Sweet's Present 6": LocData(79, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT7 - Antidote
    "Sweet's Present 7": LocData(80, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT8 - Rope
    "Sweet's Present 8": LocData(81, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT9 - Magic Herb
    "Sweet's Present 9": LocData(82, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT10 - ButterKnife
    "Sweet's Present 10": LocData(83, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT11 - Magic Herb
    "Sweet's Present 11": LocData(84, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT12 - Magic Herb
    "Sweet's Present 12": LocData(85, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT13 - PhysicalCap
    "Sweet's Present 13": LocData(86, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT14 - LifeUpCream
    "Sweet's Present 14": LocData(87, "Merrysville"),
    #OBJ_SWEETFACTORY_PRESENT15 - Antidote
    "Sweet's Present 15": LocData(88, "Merrysville"),
    #OBJ_SWEETFACTORY_BOTTLEROCKETS - 0x61 - BottlRocket
    "Sweet's Trashcan": LocData(89, "Merrysville"),

    #OBJ_MERRYSVILLE_FOODSVENDOR
	#OrangeJuice
	#Bread
	#SportsDrink
	#Null
    "Merrysville Foods 1": LocData(90, "Merrysville"),
    "Merrysville Foods 2": LocData(91, "Merrysville"),
    "Merrysville Foods 3": LocData(92, "Merrysville"),
    "Merrysville Foods 4": LocData(93, "Merrysville"),

    #OBJ_MERRYSVILLE_SPORTSVENDOR
	#Wooden Bat
	#AluminumBat
	#Boomerang
	#Null
    "Merrysville Sports 1": LocData(94, "Merrysville"),
    "Merrysville Sports 2": LocData(95, "Merrysville"),
    "Merrysville Sports 3": LocData(96, "Merrysville"),
    "Merrysville Sports 4": LocData(97, "Merrysville"),

    #!Make sure to patch out PhoneCard check
    #OBJ_MERRYSVILLE_VARIETYVENDOR
	#Ruler
	#Stun Gun
	#Rope
	#Repel Ring
    "Merrysville Variety 1": LocData(98, "Merrysville"),
    "Merrysville Variety 2": LocData(99, "Merrysville"),
    "Merrysville Variety 3": LocData(100, "Merrysville"),
    "Merrysville Variety 4": LocData(101, "Merrysville"),

    #OBJ_MERRYSVILLE_PASSTRIGGER2 - 0x59 - Pass
    "Pass": LocData(102, "Merrysville"),

    #OBJ_DUNCANFACTORY_PRESENT1 - Bomb
    "Duncan's Present 1": LocData(103, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT2 - LifeUpCream
    "Duncan's Present 2": LocData(104, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT3 - QuickCapsul
    "Duncan's Present 3": LocData(105, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT4 - PhysicalCap
    "Duncan's Present 4": LocData(106, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT5 - Wisdom Caps
    "Duncan's Present 5": LocData(107, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT6 - Rope
    "Duncan's Present 6": LocData(108, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT7 - Bomb
    "Duncan's Present 7": LocData(109, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT8 - PSI Stone
    "Duncan's Present 8": LocData(110, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT9 - LifeUpCream
    "Duncan's Present 9": LocData(111, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT10 - BottlRocket
    "Duncan's Present 10": LocData(112, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT11 - Rope
    "Duncan's Present 11": LocData(113, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT12 - Bread
    "Duncan's Present 12": LocData(114, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT13 - FranklnBdge
    "Duncan's Present 13": LocData(115, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT14 - ForceCapsul
    "Duncan's Present 14": LocData(116, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT15 - Bomb
    "Duncan's Present 15": LocData(117, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT16 - Rope
    "Duncan's Present 16": LocData(118, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT17 - BottlRocket
    "Duncan's Present 17": LocData(119, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT18 - BottlRocket
    "Duncan's Present 18": LocData(120, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT19 - Super Spray
    "Duncan's Present 19": LocData(121, "Merrysville"),
    #OBJ_DUNCANFACTORY_PRESENT20 - Bomb
    "Duncan's Present 20": LocData(122, "Merrysville"),

    #OBJ_SNOWMAN_FAKEVENDOR
	#Bread
	#Mouthwash
	#LifeUpCream
	#Frying Pan
    "Snowman Dept 1": LocData(123, "Snowman"),
    "Snowman Dept 2": LocData(124, "Snowman"),
    "Snowman Dept 3": LocData(125, "Snowman"),
    "Snowman Dept 4": LocData(126, "Snowman"),


    #OBJ_REINDEER_FOODSVENDOR
	#OrangeJuice
	#Bread
	#SportsDrink
	#berry Tofu
    "Reindeer Foods 1": LocData(128, "Reindeer"),
    "Reindeer Foods 2": LocData(129, "Reindeer"),
    "Reindeer Foods 3": LocData(130, "Reindeer"),
    "Reindeer Foods 4": LocData(131, "Reindeer"),

    #OBJ_REINDEER_SPORTSVENDOR
	#AluminumBat
	#Boomerang
	#Null
	#Null
    "Reindeer Sports 1": LocData(132, "Reindeer"),
    "Reindeer Sports 2": LocData(133, "Reindeer"),
    "Reindeer Sports 3": LocData(134, "Reindeer"),
    "Reindeer Sports 4": LocData(135, "Reindeer"),

    #OBJ_REINDEER_WEAPONVENDOR
	#Bomb
	#Laser Beam
	#Plasma Beam
	#Null
    "Reindeer Weapons 1": LocData(136, "Reindeer"),
    "Reindeer Weapons 2": LocData(137, "Reindeer"),
    "Reindeer Weapons 3": LocData(138, "Reindeer"),
    "Reindeer Weapons 4": LocData(139, "Reindeer"),

    #OBJ_REINDEER_ANAHATWOMAN - 0x62 - Hat
    "Hat": LocData(140, "Reindeer"),
    #OBJ_REINDEER_MISLAYSIGN - 0x63 - Dentures
    "Dentures": LocData(141, "Reindeer"),
    #OBJ_MISLAY_MOUTHWASHGUY - 0x44 - Mouthwash
    "Mouthwash Fill": LocData(142, "Reindeer"),
    #OBJ_MISLAY_MOUTHWASHKID - 0x44 - Mouthwash
    "Mouthwash Repeatable": LocData(143, "Reindeer"),
    #OBJ_REINDEER_FLEABAGGIRL - 0x1b - Flea Bag
    "Flea Bag": LocData(144, "Reindeer"),

    #OBJ_SPOOKANE_MRSROSEMARY - 0x57 - Ghost Key
    "Ghost Key": LocData(145, "Spookane"),

    #OBJ_ROSEMARYHOUSE_PRESENT1 - LifeUpCream
    "Mansion Present 1": LocData(146, "Rosemary Mansion"),
    #OBJ_ROSEMARYHOUSE_PRESENT2 - Antidote
    "Mansion Present 2": LocData(147, "Rosemary Mansion"),
    #OBJ_ROSEMARYHOUSE_PRESENT3 - Bread
    "Mansion Present 3": LocData(148, "Rosemary Mansion"),
    #OBJ_ROSEMARYHOUSE_PRESENT4 - Antidote
    "Mansion Present 4": LocData(149, "Rosemary Mansion"),
    #OBJ_ROSEMARYHOUSE_PRESENT5 - Null
    "Mansion Present 5": LocData(150, "Rosemary Mansion"),
    #OBJ_ROSEMARYHOUSE_PRESENT6 - LifeUpCream
    "Mansion Present 6": LocData(151, "Rosemary Mansion"),

    "Piano Melody": LocData(152, "Rosemary Mansion"),

    #OBJ_YUCCA_PILOT - 0x64 - Ticket Stub
    "Ticket Stub 1": LocData(153, "Yucca Desert"),

    "Cactus Melody": LocData(154, "Yucca Desert"),

    #OBJ_MCAVE_QUICKMONKEY - 0x4e - QuickCapsul
    "Monkey Capsule": LocData(155, "Monkey Cave"),
    #OBJ_MCAVE_PRESENT1 - PSI Stone
    "Monkey Present 1": LocData(156, "Monkey Cave"),
    #OBJ_MCAVE_PRESENT2 - PSI Stone
    "Monkey Present 2": LocData(157, "Monkey Cave"),
    #OBJ_MCAVE_PRESENT3 - PSI Stone
    "Monkey Present 3": LocData(158, "Monkey Cave"),

    #OBJ_YOUNGTOWN_FAKEDEPTVENDOR
	#Bread
	#LifeUpCream
	#NonstickPan
	#Air Gun
    "Youngtown Dept 1": LocData(159, "Youngtown"),
    "Youngtown Dept 2": LocData(160, "Youngtown"),
    "Youngtown Dept 3": LocData(161, "Youngtown"),
    "Youngtown Dept 4": LocData(162, "Youngtown"),

    #OBJ_ELLAY_FOODSVENDOR
	#OrangeJuice
	#Bread
	#SportsDrink
	#berry Tofu
    "Ellay Foods 1": LocData(163, "Ellay"),
    "Ellay Foods 2": LocData(164, "Ellay"),
    "Ellay Foods 3": LocData(165, "Ellay"),
    "Ellay Foods 4": LocData(166, "Ellay"),

    #OBJ_ELLAY_VARIETYVENDOR
	#Ticket
	#ButterKnife
	#Rope
	#Surv.Knife
    "Ellay Variety 1": LocData(167, "Ellay"),
    "Ellay Variety 2": LocData(168, "Ellay"),
    "Ellay Variety 3": LocData(169, "Ellay"),
    "Ellay Variety 4": LocData(170, "Ellay"),

    #OBJ_ELLAY_TICKETGUY - 0x5a - Ticket
    "Ellay Ticket": LocData(171, "Ellay"),

    #OBJ_ELLAY_FAKEHEALER - 0x41 - LifeUpCream
    "Ellay LifeupCream": LocData(173, "Ellay"),

    "Island Able": LocData(174, "Island"), #Doesnt give item in vanilla
    #OBJ_ISLAND_BAKER - 0x1d - Swear Words
    "Island Baker": LocData(175, "Island"),
    #OBJ_ISLAND_SCIENTIST - 0x1c - WordsO'Love
    "Island Scientist": LocData(176, "Island"),

    #OBJ_MTITOI_CAVEPRESENT1 - Katana
    "CoMI Present 1": LocData(177, "Mt. Itoi"),
    #OBJ_MTITOI_CAVEPRESENT2 - IronSkillet
    "CoMI Present 2": LocData(178, "Mt. Itoi"),
    #OBJ_MTITOI_CAVEPRESENT3 - Hank's Bat
    "CoMI Present 3": LocData(179, "Mt. Itoi"),
    #OBJ_MTITOI_CAVEPRESENT4 - LifeUpCream
    "CoMI Present 4": LocData(180, "Mt. Itoi"),
    #OBJ_MTITOI_CAVEPRESENT5 - Bomb
    "CoMI Present 5": LocData(181, "Mt. Itoi"),
    #OBJ_MTITOI_CAVEPRESENT6 - PSI Stone
    "CoMI Present 6": LocData(182, "Mt. Itoi"),

    #OBJ_MTITOI_PRESENT - Sea Pendant
    "Mt. Itoi Present": LocData(183, "Mt. Itoi"),

    #"Recruit EVE": LocData(184, "Mt. Itoi"),

    "EVE Melody": LocData(185, "Mt. Itoi"),

    "Tombstone Melody": LocData(186, "Mt. Itoi"),

}

extra_locations = {
    #"ml7's house": LocData(187, "Sibiu"),
}

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
    "Recruit Pippi": LocData(189, "Podunk"),
    "Recruit Lloyd": LocData(72, "Merrysville"),
    "Recruit Ana": LocData(127, "Snowman"),
    "Recruit Teddy": LocData(172, "Ellay"),
    "Beat Giegue": LocData(188, "Path To Giegue")
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **mother_locations,
    **extra_locations,
    **event_locations
}