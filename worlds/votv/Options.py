from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

from .Types import VOTVGoal
from .Constants import (
    max_days,
    max_signal_locations,
    max_daily_tasks_locations,
    max_fuse_replacement_locations,
    max_server_repair_locations,
    max_transformer_repair_locations,
    max_trash_cleaning_locations
)

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in votv_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class Objective(Choice):
    """
    Determines what is the objective of the run.
    """
    display_name = "Objective"
    option_kerfur_omega = int(VOTVGoal.KERFUR_OMEGA)
    option_hell_rock = int(VOTVGoal.HELL_ROCK.value)
    option_white_argemia_plush = int(VOTVGoal.WHITE_ARGEMIA_PLUSH)
    option_black_argemia_plush = int(VOTVGoal.BLACK_ARGEMIA_PLUSH)
    option_lambert_plush = int(VOTVGoal.LAMBERT_PLUSH)
    option_green_cabinet = int(VOTVGoal.GREEN_CABINET)
    option_survive = int(VOTVGoal.SURVIVE)
    default = int(VOTVGoal.KERFUR_OMEGA)

class RequireMining(Toggle):
    """
    Determines if the Radioactive Capsule can be dug out or needs to be crafted.
    """
    display_name = "Require Mining for the Radioactive Capsule"
    default = 0

class SurviveDay(Range):
    """
    Determines the day you need to survive to if the objective is Survive.
    """
    display_name = "Survive Day"
    range_start = 1
    range_end = 50
    default = 50

class DayAsItems(Toggle):
    """
    Determines if you need to unlock days as items.
    """
    display_name = "Day As Items"
    default = 0

class ScrapRecipesAsItems(Toggle):
    """
    Determines if you need to unlock scrap recipes as items.
    """
    display_name = "Scrap Recipes As Items"
    default = 0

class SurviveDayLocations(Range):
    """
    Determines the maximum day to create "Survive Day N" location for. 0 will generate none.
    """
    display_name = "Survive Day Locations"
    range_start = 0
    range_end = max_days
    default = 5

class SignalLocations(Range):
    """
    Determines the number of "Sell Level N Signal" locations to create, one for each signal level.
    """
    display_name = "Signal Locations"
    range_start = 0
    range_end = max_signal_locations
    default = 5

class DailyTaskLocations(Range):
    """
    Determines the number of "Daily Task Done" locations to create.
    """
    display_name = "Daily Task Locations"
    range_start = 0
    range_end = max_daily_tasks_locations
    default = 5

class FuseReplacementLocations(Range):
    """
    Determines the number of "Replace Fuse" locations to create.
    """
    display_name = "Replace Fuse Locations"
    range_start = 0
    range_end = max_fuse_replacement_locations
    default = 5

class ServerRepairLocations(Range):
    """
    Determines the number of "Repair Server" locations to create.
    """
    display_name = "Repair Server Locations"
    range_start = 0
    range_end = max_server_repair_locations
    default = 5

class TransformerRepairLocations(Range):
    """
    Determines the number of "Repair Transformer" locations to create.
    """
    display_name = "Repair Transformer Locations"
    range_start = 0
    range_end = max_transformer_repair_locations
    default = 5

class TrashBagsLocations(Range):
    """
    Determines the number of "Sell 10 Full Trash Bags" locations to create.
    """
    display_name = "Trash Bags Locations"
    range_start = 0
    range_end = max_trash_cleaning_locations
    default = 5

class ShopItems(Toggle):
    """
    Determines if purchasing shop items are checks.
    """
    display_name = "Shop Items As Locations"
    default = 0

class ChickenSandwiches(Toggle):
    """
    Determines if the chicken sandwiches are included as locations.
    """
    display_name = "Chicken Sandwiches As Locations"
    default = 1

class BuriedItems(Toggle):
    """
    Determines if items that require digging out are included as locations.
    Locations required by the objective are always enabled (Example: the ball joints for Kerfur-Omega)
    """
    display_name = "Buried Items As Locations"
    default = 1

class TimeSensitive(Toggle):
    """
    Determines if locations that are in-game-time-sensitive are enabled.
    """
    display_name = "Time Sensitive Locations"
    default = 0

class FunnySetting(Toggle):
    """
    Determines if items that require the "funny setting" are included as locations and items.
    """
    display_name = "Funny Setting"
    default = 0

class ArgemiaPlushes(Choice):
    """
    Determines what argemia plushes are present as locations.
    None: No Argemia plushes
    RGB: Only the Red, Green, and Blue Argemia plushes
    RGBYCM: All the Argemia plushes except the nuclear ones (adds an item to get the "lifecrystal" signal)
    All: All the Argemia plushes
    """
    display_name = "Argemia Plushes As Locations"
    option_none = 0
    option_rgb = 1
    option_rgbycm = 2
    option_all = 3
    default = 1

class KerfurOmegaEnabled(Toggle):
    """
    Determines if Kerfur-Omega locations and items should be enabled, even if it's not the objective.
    Does not include the final location.
    """
    display_name = "Kerfur-Omega Items and Locations Enabled"
    default = 1

class HellRockEnabled(Toggle):
    """
    Determines if Hell Rock locations and items should be enabled, even if it's not the objective.
    Does not include the final location.
    """
    display_name = "Hell Rock Items and Locations Enabled"
    default = 1

class LambertPlushEnabled(Toggle):
    """
    Determines if Lambert Plush locations and items should be enabled, even if it's not the objective.
    Does not include the final location.
    """
    display_name = "Lambert Plush Items and Locations Enabled"
    default = 0

class GreenCabinetEnabled(Toggle):
    """
    Determines if Green Cabinet locations and items should be enabled, even if it's not the objective.
    Does not include the final location.
    """
    display_name = "Green Cabinet Items and Locations Enabled"
    default = 1

class TrapChance(Range):
    """
    Determines the chance for any junk item to become a trap.
    Set it to 0 for no traps.
    Range is in fact a range. You can set the limits and its default.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class VOTVOptions(PerGameCommonOptions):
    objective:                  Objective
    require_mining:             RequireMining
    survive_day:                SurviveDay
    day_as_items:               DayAsItems
    scrap_recipes_as_items:     ScrapRecipesAsItems
    survive_days_locations:     SurviveDayLocations
    signal_locations:           SignalLocations
    daily_task_locations:       DailyTaskLocations
    fuse_replacement_locations: FuseReplacementLocations
    server_repair_locations:    ServerRepairLocations
    transformer_repair_locations: TransformerRepairLocations
    trash_bags_locations:       TrashBagsLocations
    shop_items:                 ShopItems
    chicken_sandwiches:         ChickenSandwiches
    buried_items:               BuriedItems
    time_sensitive:             TimeSensitive
    funny_setting:              FunnySetting
    argemia_plushes:            ArgemiaPlushes
    kerfur_omega_enabled:       KerfurOmegaEnabled
    hell_rock_enabled:          HellRockEnabled
    lambert_plush_enabled:      LambertPlushEnabled
    green_cabinet_enabled:      GreenCabinetEnabled
    trap_chance:                TrapChance


# This is where you organize your options
# Its entirely up to you how you want to organize it
votv_option_groups: Dict[str, List[Any]] = {
    "General Options": [
        Objective,
        RequireMining,
        SurviveDay
    ],
    "Item & Locations Options": [
        DayAsItems,
        ScrapRecipesAsItems,
        SurviveDayLocations,
        SignalLocations,
        DailyTaskLocations,
        FuseReplacementLocations,
        ServerRepairLocations,
        TransformerRepairLocations,
        TrashBagsLocations,
        ShopItems,
        ChickenSandwiches,
        BuriedItems,
        TimeSensitive,
        FunnySetting,
        ArgemiaPlushes,
        KerfurOmegaEnabled,
        HellRockEnabled,
        LambertPlushEnabled,
        GreenCabinetEnabled,
        TrapChance
    ]
}
