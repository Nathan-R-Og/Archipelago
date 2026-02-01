from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in mother_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class StartingChapter(Choice):
    """
    Determines which chapter you'll start with.
    When you grab choice you'll get the associated number.
    IE: If the player chooses the sewer then when you go to call StartingChapter you'll get 3
    When displaying the options names on the site, _ will become spaces and the word option will go away.
    """
    display_name = "Starting Chapter"
    option_green_hill_zone = 1
    option_romania = 2
    option_the_sewer = 3
    default = 1

class PartyShuffle(Choice):
    """
    Determines if characters will be in the item pool.
    Off: Characters will be in their vanilla locations.
    All but Ninten: You will start with Ninten, and all other characters will be randomized.
    All: You will start with a random character, and all other characters will be randomized.
    Excludes Flying Man and EVE due to them being area based.
    """
    display_name = "Party Shuffle"
    option_off = 1
    option_all_but_ninten = 2
    option_all = 3
    default = 1

class StartingCharacter(Choice):
    """
    Determines what character you will start with.
    Only relevant if you have Party Shuffle enabled.
    """
    display_name = "Starting Character"
    option_ninten = 1
    option_ana = 2
    option_lloyd = 3
    option_teddy = 4
    option_pippi = 5
    default = 1

class StartWithTeleport(Toggle):
    """
    Determines if you start with the "Teleport" PSI ability.
    Helps if you don't want to BK immediately.
    """
    display_name = "Start With Teleport"
    default = 1

class ExtraLocations(Toggle):
    """
    This will enable the extra locations option. Toggle is just true or false.
    """
    display_name = "Add Extra Locations"


class NoTrainTrainpath(Toggle):
    """
    Whether or not traversing the entire Merrysville - Reindeer train path by foot
    is in logic or not.
    Defaults to false for your sanity.
    """
    display_name = "Include Trainpath Trek"
    default = 0

class ExpModifier(Range):
    """
    Modifies the game's level curves.
    The higher the number, the less levels you will get per exp. (inversely proportional)

    150 is value used by Teddy and Pippi, which is good for default.
    -1 can be used to turn off this setting.
    """
    display_name = "Exp Modifier"
    range_start = -1
    range_end = 255
    default = 150

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

class StoneOriginTrapWeight(Range):
    """
    The weight of StoneOrigin traps in the trap pool.
    If recieved, instantly Petrifies a party member.
    """
    display_name = "StoneOrigin Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class PoisnNeedleTrapWeight(Range):
    """
    The weight of PoisnNeedle traps in the trap pool.
    If recieved, instantly Poisons a party member.
    """
    display_name = "PoisnNeedle Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

@dataclass
class MOTHEROptions(PerGameCommonOptions):
    StartingChapter:            StartingChapter
    ExtraLocations:             ExtraLocations
    PartyShuffle:               PartyShuffle
    StartingCharacter:          StartingCharacter
    StartWithTeleport:          StartWithTeleport
    NoTrainTrainpath:           NoTrainTrainpath
    ExpModifier:                ExpModifier
    TrapChance:                 TrapChance
    StoneOriginTrapWeight:      StoneOriginTrapWeight
    PoisnNeedleTrapWeight:      PoisnNeedleTrapWeight

# This is where you organize your options
# Its entirely up to you how you want to organize it
mother_option_groups: Dict[str, List[Any]] = {
    "General Options": [StartingChapter, ExtraLocations, NoTrainTrainpath,
                        PartyShuffle, StartingCharacter, StartWithTeleport,
                        ExpModifier],
    "Trap Options": [TrapChance, StoneOriginTrapWeight, PoisnNeedleTrapWeight]
}