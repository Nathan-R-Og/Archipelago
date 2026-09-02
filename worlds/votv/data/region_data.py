from typing import NamedTuple

from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachRegion, Has, HasAll, Rule, True_
from worlds.votv.Options import DayAsItems, DoorsAsItems, FenceClimbing
from worlds.votv.Utils import DayItemFieldResolver

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

def fence_entrance(connected_region: str, also: Rule = True_(), one_way: bool = False) -> EntranceInfo:
    return EntranceInfo(
        connected_region,
        connected_region,
        access_rule=also & Has(f"Half Hook", options=[OptionFilter(FenceClimbing, True)], filtered_resolution=True),
        two_way=not one_way
    )

class RegionInfo(NamedTuple):
    exits: list[EntranceInfo]

regions = {
    "Outside": RegionInfo([
        EntranceInfo("Alpha Base Entrance", "Alpha Base", two_way=True),
        door_entrance("Bunker", also=Has("Bunker Keycard")),
        door_entrance("TR1 Room"),
        door_entrance("TR2 Room"),
        door_entrance("TR3 Room"),
        EntranceInfo("Climb up", "Alpha Roof", access_rule=Has("Half Hook")),
        EntranceInfo("Dive under", "Lake", access_rule=HasAll("Scuba Mask", "Scuba Mask Tank")),
        EntranceInfo("Open the cave", "Cave", access_rule=CanReachRegion("Signal Lab") & CanReachRegion("Alpha Stairs") | Has("Day", DayItemFieldResolver(3), options=[OptionFilter(DayAsItems, True)], filtered_resolution=True)),
        fence_entrance("New Trees Area"),
        fence_entrance("Restricted Area"),
        fence_entrance("Stonehenge"),
        fence_entrance("Green Hatch"),
        fence_entrance("Abandoned Shack")
    ]),
    "Lake": RegionInfo([
        EntranceInfo("Emerge", "Outside")
    ]),
    "Cave": RegionInfo([
        EntranceInfo("Exit the cave", "Outside")
    ]),
    "New Trees Area": RegionInfo([]),
    "Restricted Area": RegionInfo([]),
    "Stonehenge": RegionInfo([]),
    "Green Hatch": RegionInfo([]),
    "Abandoned Shack": RegionInfo([]),

    "Alpha Base": RegionInfo([
        EntranceInfo("Signal Lab Entrance", "Signal Lab", two_way=True),
        door_entrance("Break Room"),
        door_entrance("Utility Closet"),
        EntranceInfo("Alpha Stairs Entrance", "Alpha Stairs", two_way=True),
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
        EntranceInfo("Garage door", "Outside")
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