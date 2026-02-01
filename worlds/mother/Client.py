import base64
import logging

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write, display_message

logger = logging.getLogger("Client")

from .Locations import location_table
from .Items import item_table, event_items, party_items
from .rom_data import rom_item_table, all_object_codes, \
all_present_flags, all_story_flags
from .Types import starting_character_table

class MOTHERClient(BizHawkClient):
    system = ("NES")
    patch_suffix = ".apebb"
    game = "MOTHER"


    variables = {
        #"party_members": (0x1408, 3, "WRAM"),
        "PlayerName": (0x1420, 0x10, "WRAM"),
        "StoryFlags": (0x1600, 0x20, "WRAM"),
        "PresentFlags": (0x1620, 0x20, "WRAM"),
        "COLLECTEDITEMS": (0x13e0-6, 6, "WRAM"),
        "APIn": (0x13e0, 0x10, "WRAM"),
        "APOut": (0x13f0, 5, "WRAM"),
        "APInParty": (0x13f0+6, 1, "WRAM"),
        "music_bank": (0x07, 1, "RAM"),
    }

    def __init__(self):
        super().__init__()
        self.locations_array = []
        self.recieved_items = []
        self.previous_level = None

        self.init_to_merrsyville = False

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x3FFE0, 0x10, "PRG ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name != "EARTH BOUND 1.00":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        return True

    #async def set_auth(self, ctx):
    #    auth_name = await read(ctx.bizhawk_ctx, [(0x77777, 21, "ROM")])
    #    auth_name = base64.b64encode(auth_name[0]).decode()
    #    ctx.auth = auth_name

    def cliprint(self, string):
        logger.log(1, string)

    async def bizprint(self, string, ctx):
        await display_message(ctx, string)

    async def game_watcher(self, ctx):
        await super().game_watcher(ctx)

        locations_checked = []
        data_writes = []

        ram_variables = {}
        args = await read(ctx.bizhawk_ctx, list(self.variables.values()))

        i = 0
        for value in args:
            name = list(self.variables.keys())[i]
            ram_variables[name] = value
            #self.cliprint(name)
            #self.cliprint(value.hex())
            i += 1

        #wait until game started
        if ram_variables["PlayerName"] != bytearray([0xFF] * 0x10):

            #workaround for flag 135
            if not self.init_to_merrsyville:
                data_writes.append((0x1610, [1], "WRAM"))
                self.init_to_merrsyville = True

            #workaround for win con
            #check for switch to credits music bank
            if ram_variables["music_bank"][0] == 0x1b:
                locations_checked.append(locations_checked.append(location_table["Beat Giegue"].ap_code))
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            def binaryFlags_to_dict(bin) -> dict:
                ram_flags = {}
                binary_string = ''.join(f'{byte:08b}' for byte in bin)
                i = 0
                while i < len(binary_string):
                    ram_flags[i] = bool(int(binary_string[i]))
                    i += 1
                return ram_flags

            def check_flags(in_dict, in_locs) -> dict:
                for key in list(in_dict.keys()):
                    if in_dict[key] and key in list(in_locs.keys()):
                        value = in_locs[key]
                        if value in list(location_table.keys()):
                            locations_checked.append(location_table[value].ap_code)

                            #self.cliprint(value)
            ram_flags = binaryFlags_to_dict(ram_variables["PresentFlags"])
            check_flags(ram_flags, all_present_flags)
            ram_story_flags = binaryFlags_to_dict(ram_variables["StoryFlags"])
            check_flags(ram_story_flags, all_story_flags)


            send_item = ram_variables["APOut"]
            if send_item[0] == 0x39:
                ram = int.from_bytes(send_item[1:3], 'little')
                bank = send_item[3]

                choicer = send_item[4]

                outp = f"Object bank {hex(bank)}:{hex(ram)} at choicer {choicer} check!"
                outp2 = f"({hex(bank)}, {hex(ram)}, {choicer})"
                await self.bizprint(outp, ctx.bizhawk_ctx)
                self.cliprint(outp)
                self.cliprint(outp2)

                to_compare = (bank, ram)
                to_compare_c = (bank, ram, choicer)
                for data in list(all_object_codes.keys()):

                    match = False
                    #include choicer
                    if len(data) > 2:
                        match = data == to_compare_c
                    else:
                        match = data == to_compare

                    if match:
                        value = all_object_codes[data]
                        await self.bizprint(value, ctx.bizhawk_ctx)
                        locations_checked.append(location_table[value].ap_code)
                        break

                #cleanup
                new = list(self.variables["APOut"])
                new[1] = [0xff] * new[1]
                data_writes.append(new)

        #receival handler
        self.recieved_items = ctx.items_received

        #internal rom collected items counter
        #literally required
        counter = int.from_bytes(ram_variables["COLLECTEDITEMS"], 'little')
        if counter == 0xFFFFFFFFFFFF:
            counter = 0

        #if mismatch, update as needed
        if len(self.recieved_items) > counter:
            #figure out how to give items
            wip_apin = bytearray(ram_variables["APIn"])
            #while
            #1. there is room in queue
            #2. you are below the recieved item count
            #keep adding items to queue
            while wip_apin.count(0xFF) > 0 and len(self.recieved_items) > counter:
                the_item = self.recieved_items[counter]

                #get item name
                ret_name = ""
                for item in list(item_table.keys()):
                    if item_table[item].ap_code == the_item.item:
                        ret_name = item
                        break
                if ret_name == "":
                    self.cliprint("how")

                #if the location is from a non-item given location in base game, use multiplayer input
                if ret_name in list(event_items.keys()):
                    #event items
                    if ret_name == "Maria's Love":
                        #remove rocks
                        data_writes.append((0x141b, [123], "WRAM"))
                        counter += 1
                        continue
                    elif ret_name == "Duncan's Rocket":
                        #reenable rocket
                        #flag 113
                        byte = 0
                        ram_story_flags[113] = True
                        for i in range(8):
                            the_bool = ram_story_flags[112+i]
                            byte |= int(the_bool) << (7 - i)
                        data_writes.append((0x162, [byte], "WRAM"))
                        counter += 1
                        continue
                    elif ret_name == "Duncan's Rocket":
                        #give generic bottle rocket
                        ret_name = "BottlRocket"
                    else:
                        counter += 1
                        continue

                elif ret_name in list(party_items.keys()):
                    the_id = -1
                    for id in list(starting_character_table.keys()):
                        if starting_character_table[id] == ret_name:
                            the_id = id
                            break

                    #check if you current have room for more party members
                    members_copy = bytearray(ram_variables["APInParty"])
                    if members_copy[0] == 0xFF:
                        members_copy[0] = the_id
                        new = list(self.variables["APInParty"])
                        new[1] = members_copy
                        data_writes.append(new)
                    else:
                        ram_story_flags[the_id+1] = True
                        byte = 0
                        for i in range(8):
                            the_bool = ram_story_flags[i]
                            byte |= int(the_bool) << (7 - i)
                        data_writes.append((0x160, [byte], "WRAM"))

                    counter += 1
                    continue


                #all of this only matters if the item is for this world (and not an event item)
                if the_item.player == ctx.slot:
                    self.cliprint("GOT ITEM FOR SELF!! HANDLE NOW")

                    #get item name
                    ret_loc_name = ""
                    for location in list(location_table.keys()):
                        if location_table[location].ap_code == the_item.location:
                            ret_loc_name = location
                            break
                    if ret_loc_name == "":
                        self.cliprint("how")

                    if ret_loc_name in list(all_story_flags.values()):
                        self.cliprint("ITEM IS OKAY TO GIVE!!")
                    else:
                        self.cliprint("ITEM IS NOT OKAY TO GIVE!!")
                        self.cliprint("IT IS GIVEN THROUGH AN ITEM GIVER!!")
                        self.cliprint("IMPLEMENT PROPERLY DICKHEAD!!")
                        counter += 1
                        continue

                #at this point, an item is okay to be given to the player
                #check against actual rom data to make sure it is a valid item
                self.cliprint(f"got item {ret_name}")
                rom_item_id = 0xff
                if ret_name in list(rom_item_table.keys()):
                    rom_item_id = rom_item_table[ret_name].rom_id
                else:
                    self.cliprint("lmfao/. not implemented yet :)")
                    counter += 1
                    continue

                #add to queue
                wip_apin[wip_apin.index(0xFF)] = rom_item_id
                counter += 1

            #cleanup
            #write back to emulator
            new = list(self.variables["APIn"])
            new[1] = wip_apin
            data_writes.append(new)

            #update the count!!
            new = list(self.variables["COLLECTEDITEMS"])
            new[1] = int.to_bytes(counter, 6, 'little')
            data_writes.append(new)

        #first item in queue has been collected. shift forward
        elif ram_variables["APIn"][0] == 0xFF:
            new = list(self.variables["APIn"])
            new[1] = bytearray(ram_variables["APIn"])
            new[1].pop(0)
            new[1].append(0xFF)
            data_writes.append(new)

        #write to emu
        if len(data_writes) > 0:
            success = await write(ctx.bizhawk_ctx, data_writes)

        #if not connected, dont checkloc
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        if len(locations_checked) > 0:
            self.locations_array = locations_checked
            await ctx.check_locations(locations_checked)

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)
        #if cmd == 'Connected':
        #    if ctx.slot_data["energy_link"]:
        #        ctx.set_notify(f"EnergyLink{ctx.team}")
        #        if ctx.ui:
        #            ctx.ui.enable_energy_link()
        #            ctx.ui.energy_link_label.text = "Lives: Standby"
        #elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
        #    if ctx.ui:
        #        ctx.ui.energy_link_label.text = f"Lives: {int(args['value'] / BANK_EXCHANGE_RATE)}"
        #elif cmd == "Retrieved":
        #    if f"EnergyLink{ctx.team}" in args["keys"] and args['keys'][f'EnergyLink{ctx.team}'] and ctx.ui:
        #        ctx.ui.energy_link_label.text = f"Lives: {int(args['keys'][f'EnergyLink{ctx.team}'] / BANK_EXCHANGE_RATE)}"
