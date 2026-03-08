from enum import IntEnum
from typing import Any, NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class GHSLocation(Location):
    game = "Gregory Horror Show"

class GHSItem(Item):
    game = "Gregory Horror Show"

class EpisodeType(IntEnum):
    TOT = 1
    SSE = 2
    VV = 3
    FITS = 4
    CHOH = 5
    ALL = 6


# BASE ID FOR GAME
BASE_ID = 96200200

# ITEM ID OFFSET FOR GAME
ITEM_OFFSET = 0

class ItemData(NamedTuple):
    base_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1
    @property
    def ap_code(self):
        if self.base_code == None:
            return None
        #ADD OFFSET
        return self.base_code + BASE_ID + ITEM_OFFSET

# LOCATION ID OFFSET FOR GAME
EVENT_OFFSET = 4000
class EventData(NamedTuple):
    name:       str
    base_code:    Optional[int] = None
    @property
    def ap_code(self):
        if self.base_code == None:
            return None
        #ADD OFFSET
        return self.base_code + BASE_ID + EVENT_OFFSET

# LOCATION ID OFFSET FOR GAME
LOC_OFFSET = 1000
class LocData(NamedTuple):
    base_code: Optional[int]
    region: Optional[str]
    key_type: Optional[EpisodeType] = None
    key_requirement: Optional[int] = 0
    level_type: Optional[str] = None
    @property
    def ap_code(self):
        if self.base_code == None:
            return None
        #ADD OFFSET
        return self.base_code + BASE_ID + LOC_OFFSET

class LevelData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
    bottle_amount: Optional[int]

episode_type_to_name = {
    EpisodeType.TOT:      "Tide of Terror",
    EpisodeType.SSE:      "Sunset Snake Eyes",
    EpisodeType.VV:       "Vicious Voodoo",
    EpisodeType.FITS:     "Fire in the Sky",
    EpisodeType.CHOH:     "Cold Heart of Hate",
    EpisodeType.ALL:      "All"
}

episode_type_to_shortened_name = {
    EpisodeType.TOT:    "ToT",
    EpisodeType.SSE:    "SSE",
    EpisodeType.VV:     "VV",
    EpisodeType.FITS:   "FitS",
    EpisodeType.CHOH:   "CHoH",
    EpisodeType.ALL:    "All"
}