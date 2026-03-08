from .Types import LocData, EpisodeType, LevelData, GHSLocation
from typing import Dict, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from . import GHSWorld

def did_include_hourglasses(world: "GHSWorld") -> bool:
    return bool(world.options.IncludeHourglasses)

def hourglasses_roll(world: "GHSWorld") -> bool:
    return bool(world.options.HourglassesRequireRoll)

def did_avoid_early_bk(world: "GHSWorld") -> bool:
    return bool(world.options.AvoidEarlyBK)

def get_total_locations(world: "GHSWorld") -> int:
    total = 0
    for name in location_table:
        if not did_include_hourglasses(world) and name in hourglass_locations:
            continue

        if location_table[name].level_type in world.options.ExcludeMinigames.value:
            continue

        if is_valid_location:
            total += 1

    if world.options.LocationCluesanityBundleSize.value > 0:
            for name in bottle_amounts.keys():
                bundle_amount = get_bundle_amount_for_level(name, world.options.LocationCluesanityBundleSize.value)

                total += bundle_amount

    for name, data in minigame_locations.items():
        if data.level_type in world.options.ExcludeMinigames.value:
            continue

        total += world.options.MinigameCaches.value

    return total

def get_location_names() -> Dict[str, int]:
    # There HAS to be a better way. I just dont know it since I can't pass the world in here so I can't check the options

    # For all possible bottle numbers, create location entries
    all_possible_bottle_locations = {}
    for name, data in bottle_amounts.items():
        for bottle_number in range(1, data.bottle_amount + 1):
            bottle_code = data.ap_code + (bottle_number - 1)
            bottle_location_name = f"{name} Bottle #{bottle_number}"
            all_possible_bottle_locations[bottle_location_name] = bottle_code

    # Add all the normal key minigame locations and all the cache options
    all_possible_minigame_locations = {}
    for name, data in minigame_locations.items():
        base_name = name.removesuffix(" Key")
        for cache_number in range(1, 11):
            cache_code = data.ap_code + cache_number
            cache_location_name = f"{base_name} Cache #{cache_number}"
            all_possible_minigame_locations[cache_location_name] = cache_code

    names = {**{name: data.ap_code for name, data in location_table.items()}, **all_possible_bottle_locations, **all_possible_minigame_locations}

    return names

def is_valid_location(world: "GHSWorld", name) -> bool:
    if not did_include_hourglasses(world) and name in hourglass_locations:
        return False

    if location_table[name].level_type in world.options.ExcludeMinigames.value:
        return False

    if world.options.LocationCluesanityBundleSize.value == 0 and 'Bottle' in name:
        return False

    return True

def get_bundle_amount_for_level(level_name: str, bundle_size: int) -> int:
    level_data = bottle_amounts[level_name]

    bundle_amount = int(level_data.bottle_amount/bundle_size)
    if level_data.bottle_amount%bundle_size != 0:
        bundle_amount += 1

    return bundle_amount

def generate_bottle_locations(world: "GHSWorld", bundle_size: int) -> Dict[str, LocData]:
    for name, data in bottle_amounts.items():
        bundle_amount = get_bundle_amount_for_level(name, bundle_size)

        reg = world.multiworld.get_region(data.region, world.player)

        for x in range(1, bundle_amount + 1):
            bottle_number = bundle_size * x
            if bottle_number > data.bottle_amount:
                bottle_number = data.bottle_amount
            bottle_code = data.ap_code + (bottle_number - 1)
            # Delete every bottle so we can add only the ones that are valid
            bottle_name = f"{name} Bottle #{bottle_number}"
            if bottle_name in location_table:
                del location_table[bottle_name]

            location = GHSLocation(world.player, bottle_name, bottle_code, reg)
            reg.locations.append(location)

def generate_minigame_locations(world: "GHSWorld", cache_size: int) -> Dict[str, LocData]:
    for name, data in minigame_locations.items():
        if data.level_type in world.options.ExcludeMinigames.value:
            continue

        reg = world.multiworld.get_region(data.region, world.player)
        base_name = name.removesuffix(" Key")

        # Add cache locations if cache_size > 0
        if cache_size > 0:
            for cache_number in range(1, cache_size + 1):
                cache_name = f"{base_name} Cache #{cache_number}"
                cache_code = data.ap_code + cache_number
                cache_location = GHSLocation(world.player, cache_name, cache_code, reg)
                reg.locations.append(cache_location)

sly_locations = {
    "Paris Files": LocData(000, "Paris",),

    ## Key Locations - Finishing the level
    # Tide of Terror
    "Stealthy Approach Key": LocData(101, "Stealthy Approach", key_type=EpisodeType.TOT),
    "Into the Machine Key": LocData(102, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Key": LocData(103, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Key": LocData(104, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Key": LocData(105, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Key": LocData(106, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(108, "Rocky Start", key_type=EpisodeType.SSE),
    "Boneyard Casino Key": LocData(111, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Key": LocData(112, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Key": LocData(113, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Key": LocData(114, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(115, "Dread Swamp Path", key_type=EpisodeType.VV),
    "Lair of the Beast Key": LocData(116, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Key": LocData(117, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Key": LocData(119, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(122, "Perilous Ascent", key_type=EpisodeType.FITS),
    "Unseen Foe Key": LocData(123, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Key": LocData(124, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Key": LocData(128, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),

    ## Boss Victories
    "Eye of the Storm": LocData(229, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Last Call": LocData(230, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Deadly Dance": LocData(231, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Flame Fu!": LocData(232, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
}

hourglass_locations = {
    ## Hourglass Locations - Speedrunning the level
    # Tide of Terror
    "Stealthy Approach Hourglass": LocData(301, "Stealthy Approach", key_type=EpisodeType.TOT, key_requirement = 1),
    "Into the Machine Hourglass": LocData(302, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Hourglass": LocData(303, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Hourglass": LocData(304, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Hourglass": LocData(305, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Hourglass": LocData(306, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Hourglass": LocData(308, "Rocky Start", key_type=EpisodeType.SSE, key_requirement = 1),
    "Boneyard Casino Hourglass": LocData(311, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Hourglass": LocData(312, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Hourglass": LocData(313, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Hourglass": LocData(314, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Hourglass": LocData(315, "Dread Swamp Path", key_type=EpisodeType.VV, key_requirement = 1),
    "Lair of the Beast Hourglass": LocData(316, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Hourglass": LocData(317, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Hourglass": LocData(319, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Hourglass": LocData(322, "Perilous Ascent", key_type=EpisodeType.FITS, key_requirement = 1),
    "Unseen Foe Hourglass": LocData(323, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Hourglass": LocData(324, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Hourglass": LocData(328, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),
}

vault_locations = {
    ## Vault Locations - Collecting all bottles in level
    # Tide of Terror
    "Stealthy Approach Vault": LocData(201, "Stealthy Approach", key_type=EpisodeType.TOT),
    "Into the Machine Vault": LocData(202, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Vault": LocData(203, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Vault": LocData(204, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Vault": LocData(205, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Vault": LocData(206, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(208, "Rocky Start", key_type=EpisodeType.SSE),
    "Boneyard Casino Vault": LocData(211, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Vault": LocData(212, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Vault": LocData(213, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Vault": LocData(214, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(215, "Dread Swamp Path", key_type=EpisodeType.VV),
    "Lair of the Beast Vault": LocData(216, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Vault": LocData(217, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Vault": LocData(219, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(222, "Perilous Ascent", key_type=EpisodeType.FITS),
    "Unseen Foe Vault": LocData(223, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Vault": LocData(224, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Vault": LocData(228, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3)
}

minigame_locations = {
    "Treasure in the Depths Key": LocData(1000, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3, level_type = "Crabs"),
    "At the Dog Track Key": LocData(1100, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1, level_type = "Races"),
    "Murray's Big Gamble Key": LocData(1200, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1, level_type = "Turrets"),
    "Piranha Lake Key": LocData(1300, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1, level_type = "Swamp Skiff"),
    "Ghastly Voyage Key": LocData(1400, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3, level_type = "Hover Blasters"),
    "Down Home Cooking Key": LocData(1500, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3, level_type = "Chicken Killing"),
    "King of the Hill Key": LocData(1600, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1, level_type = "Turrets"),
    "Rapid Fire Assault Key": LocData(1700, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3, level_type = "Hover Blasters"),
    "Desperate Race Key": LocData(1800, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3, level_type = "Races")
}

event_locations = {
    "Beat Raleigh": LocData(None, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Beat Muggshot": LocData(None, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Beat Mz. Ruby": LocData(None, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Beat Panda King": LocData(None, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
    "Beat Clockwerk": LocData(233, "Cold Heart of Hate", key_type=EpisodeType.CHOH)
}

bottle_amounts = {
    "Stealthy Approach":      LevelData(400, "Stealthy Approach", 20),
    "Into the Machine":         LevelData(420, "Into the Machine", 30),
    "High Class Heist":         LevelData(450, "High Class Heist", 30),
    "Fire Down Below":      LevelData(480, "Fire Down Below", 30),
    "Cunning Disguise":       LevelData(510, "Cunning Disguise", 30),
    "Gunboat Graveyard":    LevelData(540, "Gunboat Graveyard", 20),

    "Rocky Start":            LevelData(560, "Rocky Start", 40),
    "Boneyard Casino":          LevelData(600, "Boneyard Casino", 40),
    "Straight to the Top":      LevelData(640, "Straight to the Top", 40),
    "Two to Tango":             LevelData(680, "Two to Tango", 30),
    "Back Alley Heist":         LevelData(710, "Back Alley Heist", 30),

    "Dread Swamp Path":     LevelData(740, "Dread Swamp Path", 20),
    "Lair of the Beast":    LevelData(760, "Lair of the Beast", 30),
    "Grave Undertaking":      LevelData(790, "Grave Undertaking", 40),
    "Descent into Danger":      LevelData(830, "Descent into Danger", 40),

    "Perilous Ascent":        LevelData(870, "Perilous Ascent", 30),
    "Flaming Temple of Flame":  LevelData(930, "Flaming Temple of Flame", 25),
    "Unseen Foe":           LevelData(900, "Unseen Foe", 30),
    "Duel by the Dragon":       LevelData(955, "Duel by the Dragon", 40)
}

location_table = {
    **sly_locations,
    **vault_locations,
    **hourglass_locations,
    **event_locations,
    **minigame_locations,
}