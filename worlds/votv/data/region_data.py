from typing import NamedTuple

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, True_
from worlds.votv.Options import DoorsAsItems

class EntranceInfo(NamedTuple):
    name: str
    connected_region: str
    access_rule: Rule | None = None
    hide_path: bool = False
    two_way: bool = False

def door_entrance(connected_region: str, item: str = "", also: Rule = True_(), one_way: bool = False) -> EntranceInfo :
    return EntranceInfo(
        connected_region,
        connected_region,
        access_rule=also & Has(f"{connected_region} Entrance" if len(item) == 0 else item, options=[OptionFilter(DoorsAsItems, True)], filtered_resolution=True),
        two_way=not one_way
    )

class RegionInfo(NamedTuple):
    exits: list[EntranceInfo]

regions = {
    "Outside": RegionInfo([
        door_entrance("Alpha Base"),
        door_entrance("Bunker", also=Has("Bunker Keycard")),
        door_entrance("TR1 Room"),
        door_entrance("TR2 Room"),
        door_entrance("TR3 Room"),
        EntranceInfo("Climb up", "Alpha Roof", access_rule=Has("Half Hook")),
        EntranceInfo("Dive under", "Lake", access_rule=HasAll("Scuba Mask", "Scuba Mask Tank"))
    ]),
    "Lake": RegionInfo([
        EntranceInfo("Emerge", "Outside")
    ]),

    "Alpha Base": RegionInfo([
        door_entrance("Signal Lab"),
        door_entrance("Break Room"),
        door_entrance("Utility Closet"),
        door_entrance("Alpha Stairs")
    ]),
    "Signal Lab": RegionInfo([
        door_entrance("Server Room")
    ]),
    "Server Room": RegionInfo([]),
    "Break Room": RegionInfo([]),
    "Utility Closet": RegionInfo([]),
    "Garage": RegionInfo([
        door_entrance("Admin Room"),
        EntranceInfo("Climb out", "Alpha Roof", access_rule=Has("Half Hook")),
        EntranceInfo("Elevator", "Storage Room", two_way=True),
        EntranceInfo("Garage Door", "Outside")
    ]),
    "Admin Room": RegionInfo([]),
    "Alpha Stairs": RegionInfo([
        door_entrance("Storage Room"),
        door_entrance("Staff Room"),
    ]),
    "Storage Room": RegionInfo([]),
    "Staff Room": RegionInfo([
        door_entrance("Bathroom"),
        door_entrance("Alpha Roof")
    ]),
    "Bathroom": RegionInfo([]),
    "Alpha Roof": RegionInfo([
        EntranceInfo("Drop through the roof", "Garage"),
        EntranceInfo("Drop down", "Outside"),
    ]),

    "Bunker": RegionInfo([]),

    "TR1 Room": RegionInfo([]),
    "TR2 Room": RegionInfo([]),
    "TR3 Room": RegionInfo([])
}