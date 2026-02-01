import hashlib
import os
import pkgutil

import Utils

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .Types import starting_character_table

from typing import TYPE_CHECKING, Dict, List, Tuple

from .rom_data import rom_item_table, item_place_locations

if TYPE_CHECKING:
    from . import MOTHERWorld

def generate_output(world: "MOTHERWorld", output_directory: str):
    patch = MOTHERProcedurePatch(player=world.player, player_name=world.player_name)

    patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "basepatch.bsdiff4"))

    actual_location_table = {}

    for location in world.multiworld.get_locations(world.player):
        if location.item is None:
            continue

        #get item byte
        the_item = location.item
        if the_item.player != world.player:
            #if is offworld item

            #if being placed at a character
            if location.name.startswith("Recruit"):
                the_item = 0
            else:
                the_item = 0xFF
        else:
            #if being placed at a character
            if location.name.startswith("Recruit"):
                #if item is also a character
                if the_item.name in list(starting_character_table.values()):
                    #check if location is a Recruit location. if not, then ignore
                    for id in list(starting_character_table.keys()):
                        if starting_character_table[id] == the_item.name:
                            the_item = id
                            break
                else:
                    #give party id 0
                    the_item = 0
            else:
                #if it is a real game item, make it an id
                if the_item.name in list(rom_item_table.keys()):
                    the_item = rom_item_table[the_item.name].rom_id
                else:
                    the_item = 0xFF
                    #TODO: handle event items/not actual items
                    #continue

        actual_location_table[location.name] = the_item

    for setter in list(item_place_locations.keys()):
        location_name = item_place_locations[setter]
        if location_name in list(actual_location_table.keys()):
            item = actual_location_table[location_name]
            bank, offset = setter
            patch.write_bytes((bank*0x2000) + (offset-0x8000) + 0x10, item)

    #define anchors
    save_meta = (0x18 * 0x2000) + 0x1e00 + 0x10
    starting_characters = save_meta + 0x40

    #start with teleport
    start_with_teleport = bool(world.options.StartWithTeleport.value)
    if start_with_teleport:
        ninten_learntable = starting_characters + 0x30
        ana_learntable = starting_characters + 0x30 + (1 * 0x40)
        value = 0b01100000
        patch.write_bytes(ninten_learntable, value)
        patch.write_bytes(ana_learntable, value)

    #start with anyone else
    starting_character = starting_character_table[world.options.StartingCharacter.value]
    if starting_character != "Ninten":
        #set party_members[0]
        patch.write_bytes(save_meta+8, world.options.StartingCharacter.value)

        #move cash card to this guy
        item = starting_characters + 0x20 + ((world.options.StartingCharacter.value - 1) * 0x40)
        patch.write_bytes(item, 0x6E)
        ninten_item = starting_characters + 0x20
        patch.write_bytes(ninten_item, 0)

    #write exp mod
    if world.options.ExpModifier.value != -1:
        rates = 0x1DC0 + 0x10
        for i in range(8):
            patch.write_bytes(rates + (8*i), world.options.ExpModifier.value)

    patch.write_file("tokens.bin", patch.get_token_binary())
    patch.write(os.path.join(output_directory,
                             f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))


class MOTHERProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "54387b6e68142d69083a38b437196450"
    patch_file_ending = ".apebb"
    game = "MOTHER"
    result_file_ending = ".nes"
    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["tokens.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset, value):
        if isinstance(value, int):
            value = [value]
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def get_base_rom_bytes():
    file_name = get_base_rom_path()
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if MOTHERProcedurePatch.hash != basemd5.hexdigest():
        raise Exception("Supplied Base Rom does not match known MD5 for EARTH BOUND 1.0. "
                        "Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path():
    file_name = get_settings()["mother_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
