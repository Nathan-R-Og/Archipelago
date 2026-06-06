# This file is technically not required whatsoever
# I like to do this for organization and a few other worlds do similar
# Its helpful for grouping variables, making them easy to access, and consistent

from enum import IntEnum
from typing import TYPE_CHECKING, Callable, NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

if TYPE_CHECKING:
    from . import VOTVWorld

# These 2 make it so that the generic Location and Item types are more specific for your game
class VOTVLocation(Location):
    game = "VOTV"

class VOTVItem(Item):
    game = "VOTV"

# BASE ID FOR GAME
BASE_ID = 0x4a4a1515

# ITEM ID OFFSET FOR GAME
ITEM_OFFSET = 0

# Here is where all the stuff from the Items.py comes from
# You can add or take away anything you want but ap_code and classification are pretty important
# Adding Optional[] makes it so you dont have to include it when you create an ItemData
# Adding = x at the end adds a default to it so if you dont include it, it'll default to whatever you put after it
class ItemData(NamedTuple):
    base_code: Optional[int]
    classification: dict[ItemClassification, int] | Callable[["VOTVWorld"], dict[ItemClassification, int]]

    @property
    def ap_code(self):
        #ADD OFFSET
        return (self.base_code or 0) + BASE_ID + ITEM_OFFSET

# LOCATION ID OFFSET FOR GAME
LOC_OFFSET = 1000

# Again where all the Location.py things come from
# You can add whatever you want here as well but ap_code and region are pretty important
class LocData(NamedTuple):
    base_code: Optional[int]
    region: Optional[str]

    @property
    def ap_code(self):
        #ADD OFFSET
        return (self.base_code or 0) + BASE_ID + LOC_OFFSET

class VOTVGoal(IntEnum):
    KERFUR_OMEGA = 0
    HELL_ROCK = 1
    WHITE_ARGEMIA_PLUSH = 2
    BLACK_ARGEMIA_PLUSH = 3
    LAMBERT_PLUSH = 4
    GREEN_CABINET = 5
    SURVIVE = 6
